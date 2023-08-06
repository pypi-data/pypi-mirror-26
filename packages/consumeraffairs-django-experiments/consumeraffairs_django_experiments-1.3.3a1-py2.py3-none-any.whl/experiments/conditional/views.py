# coding=utf-8
from __future__ import absolute_import

import logging
from functools import wraps

logger = logging.getLogger(__name__)


class Experiments(object):
    """
    Handles everything related to evaluating conditional experiments.
    Initialised by ExperimentsMixin().
    Separate from the mixin to avoid polluting the view class namespace.
    """
    context = {}
    instances = ()
    report = {
        'auto_enroll': {}
    }

    def __init__(self, request, view):
        from ..models import Experiment

        self.request, self.view = request, view
        self._build_context()
        self.instances = Experiment.objects.filter(
            auto_enroll=True,
        )

    def _build_context(self):
        self.context.update(request=self.request)
        self.context.update(view=self.view)
        self._add_to_context(self.view, 'get_object')
        self._add_to_context(self.view, 'get_context_data')
        self._add_to_context(self.view, 'template_name')

    def get_participant(self):
        """
        Returns an instance of experiments.utile.WebUser or its subclass
        Cached on the request.
        """
        from ..utils import participant

        return participant(self.request)

    def conditionally_enroll(self):
        """
        Enroll current user in all experiments that are marked with
        `auto_enroll` and evaluate at least one of the conditionals
        positively.
        """
        for i in self.instances:
            active = i.should_auto_enroll(self.request)
            variate = None
            if active:
                variate = self.get_participant().enroll(
                    i.name, i.alternative_keys)
            self._report(i, active, variate)

    def _report(self, instance, active, variate):
        """
        Populate self.report dict, used to set cookie with
        experiments data. The cookie is useful for debugging
        and verifying whether an experiment is running.
        """
        self.report['auto_enroll'][instance.name] = {
            'experiment_active': active,
            'enrolled_variate': variate,
        }

    def _add_to_context(self, obj, method_name):
        """
        Takes an attribute or the return value of a method and adds
        it to the context.
        """
        method = getattr(obj, method_name, None)

        if method is None:
            return

        if not callable(method):
            # method is actually just an attribute
            self.context.update(**{
                method_name: method,
            })
            return

        def add_to_context(func):
            """
            Decorator, runs the method and keeps the returned value
            in `self.context` dict.
            """
            @wraps(func)
            def _decorated_func(*args, **kwargs):
                value = func(*args, **kwargs)
                self.context.update(**{
                    func.__name__: value,
                })
                return value
            return _decorated_func

        setattr(self.view, method.__name__, add_to_context(method))


class ExperimentsMixin(object):
    """Mixin for View classes (class based views)"""
    experiments = None

    def dispatch(self, request, *args, **kwargs):
        """Instantiates the Experiments object for the current request"""
        request.experiments = Experiments(request, self)
        request.experiments.conditionally_enroll()
        response = super(ExperimentsMixin, self).dispatch(
            request, *args, **kwargs)
        logger.debug('experiments.context: %s', request.experiments.context)
        return response
