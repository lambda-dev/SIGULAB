/*TRIGGER UPDATE INVENTARIO*/
CREATE OR REPLACE function update_total_inventario() RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN
    --INSERT INTO usuario VALUES (NEW.carnet,NEW.correo,NEW.nombre,NEW.apellido,NOW(),NEW.saldo);
    NEW.f_total = NEW.f_cantidadonacion+NEW.f_cantidadusointerno;
    RETURN NEW;
  ELSIF (TG_OP = 'UPDATE') THEN
    NEW.f_total = NEW.f_cantidadonacion+NEW.f_cantidadusointerno;
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_inventario_total_update BEFORE INSERT OR UPDATE ON
t_inventario FOR EACH ROW EXECUTE PROCEDURE update_total_inventario();
