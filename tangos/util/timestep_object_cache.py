from .. import core

class TimestepObjectCache(object):
    """A temporary store for all objects in a timestep, allowing objects to be resolved without a further database query"""
    def __init__(self, timestep):
        """Query the database for all objects in this timestep

        :type timestep: core.TimeStep"""

        self.session = core.Session.object_session(timestep)
        self._timestep_id = timestep.id

    def _initialise_cache(self):
        all_objects = self.session.query(core.Halo).filter_by(timestep_id=self._timestep_id).all()

        self._map_catalog = {}
        self._map_finder = {}
        for obj in all_objects:
            typetag = obj.object_typetag_from_code(obj.object_typecode)
            if typetag not in self._map_catalog:
                self._map_catalog[typetag] = {}
            if typetag not in self._map_finder:
                self._map_finder[typetag] = {}
            self._map_catalog[typetag][obj.catalog_index] = obj
            self._map_finder[typetag][obj.finder_id] = obj

    def _ensure_cache(self):
        if not hasattr(self, "_map_finder") or not hasattr(self, "_map_catalog"):
            self._initialise_cache()

    def resolve_from_catalog_index(self, catalog_index, typetag):
        self._ensure_cache()
        try:
            return self._map_catalog[typetag][catalog_index]
        except KeyError:
            return None

    def resolve_from_finder_id(self, finder_id, typetag):
        self._ensure_cache()
        try:
            return self._map_finder[typetag][finder_id]
        except KeyError:
            return None