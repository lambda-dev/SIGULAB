db.executesql('CREATE OR REPLACE function \
update_total_inventario() RETURNS TRIGGER \
AS $$ BEGIN IF (TG_OP = \'INSERT\') THEN\
 NEW.f_total = NEW.f_cantidadonacion+\
 NEW.f_cantidadusointerno; RETURN NEW; ELSIF\
  (TG_OP = \'UPDATE\') THEN NEW.f_total = \
  NEW.f_cantidadonacion+NEW.f_cantidadusointerno; \
  RETURN NEW; END IF; END; $$ LANGUAGE plpgsql;')

if(db(db.t_inventario).isempty()):
    db.executesql('CREATE TRIGGER \
    trigger_inventario_total_update BEFORE INSERT\
     OR UPDATE ON t_inventario FOR EACH ROW EXECUTE \
     PROCEDURE update_total_inventario();')
