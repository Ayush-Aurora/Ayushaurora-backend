class DoctorRouter():
    route_app_labels = {'prescriptions'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return ['medicine_data' , 'default' , 'doctors_db']
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'doctors_db'
        return None

    def allow_relations(self , object_1 , object_2 , **hints):
        if (object_1._meta.app_label in self.route_app_labels or object_2._meta.app_label in self.route_app_labels):
            return True
        return None
    
    def allow_migrate(self , db , app_label , model_name=None , **hints):
        if app_label in self.route_app_labels:
            return db == 'doctors_db'
        return None

class MedicineRouter():
    route_app_labels = {'medicines'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'medicine_data'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'medicine_data'
        return None

    def allow_relations(self , object_1 , object_2 , **hints):
        if (object_1._meta.app_label in self.route_app_labels or object_2._meta.app_label in self.route_app_labels):
            return True
        return None
    
    def allow_migrate(self , db , app_label , model_name=None , **hints):
        if app_label in self.route_app_labels:
            return db == 'medicine_data'
        return None