/*TRIGGER UPDATE INVENTARIO*/
CREATE OR REPLACE function update_cantidad_bitacora() RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN

    NEW.f_fecha = NOW();

    IF (NEW.f_ingreso != 0) THEN

      IF (EXISTS (SELECT * FROM t_inventario i INNER JOIN t_bitacora b
        ON (i.f_sustancia = b.f_sustancia AND
        i.f_espaciofisico = b.f_espaciofisico) WHERE i.f_sustancia = NEW.f_sustancia )) THEN

          NEW.f_cantidad = (SELECT f_cantidadusointerno
                            FROM t_inventario i INNER JOIN t_bitacora b
                            ON (i.f_sustancia = b.f_sustancia AND i.f_espaciofisico = b.f_espaciofisico)
                            WHERE i.f_sustancia = NEW.f_sustancia LIMIT 1) + NEW.f_ingreso;
          UPDATE t_inventario SET f_cantidadusointerno = NEW.f_cantidad
            WHERE f_sustancia = NEW.f_sustancia AND f_espaciofisico = NEW.f_espaciofisico;
          RETURN NEW;
      ELSE
        INSERT INTO t_inventario VALUES(default,NEW.f_sustancia,NEW.f_espaciofisico,0,NEW.f_ingreso);
        NEW.f_cantidad = NEW.f_ingreso;
        RETURN NEW;

      END IF;

    END IF;

    IF (NEW.f_consumo != 0) THEN

      NEW.f_cantidad = (SELECT f_cantidadusointerno
                        FROM t_inventario i INNER JOIN t_bitacora b
                        ON (i.f_sustancia = b.f_sustancia AND i.f_espaciofisico = b.f_espaciofisico)
                        WHERE i.f_sustancia = NEW.f_sustancia LIMIT 1) - NEW.f_consumo;
      UPDATE t_inventario SET f_cantidadusointerno = NEW.f_cantidad
        WHERE f_sustancia = NEW.f_sustancia AND f_espaciofisico = NEW.f_espaciofisico;
      RETURN NEW;

    END IF;

  ELSIF (TG_OP = 'UPDATE') THEN

    NEW.f_fecha = NOW();
    IF (NEW.f_ingreso != 0) THEN

          NEW.f_cantidad = (SELECT f_cantidadusointerno
                            FROM t_inventario i INNER JOIN t_bitacora b
                            ON (i.f_sustancia = b.f_sustancia AND i.f_espaciofisico = b.f_espaciofisico)
                            WHERE i.f_sustancia = NEW.f_sustancia LIMIT 1) + NEW.f_ingreso - OLD.f_ingreso;
          UPDATE t_inventario SET f_cantidadusointerno = NEW.f_cantidad
            WHERE f_sustancia = NEW.f_sustancia AND f_espaciofisico = NEW.f_espaciofisico;
          RETURN NEW;

    END IF;

    IF (NEW.f_consumo != 0) THEN

      NEW.f_cantidad = (SELECT f_cantidadusointerno
                        FROM t_inventario i INNER JOIN t_bitacora b
                        ON (i.f_sustancia = b.f_sustancia AND i.f_espaciofisico = b.f_espaciofisico)
                        WHERE i.f_sustancia = NEW.f_sustancia LIMIT 1) - NEW.f_consumo + OLD.f_consumo;
      UPDATE t_inventario SET f_cantidadusointerno = NEW.f_cantidad
        WHERE f_sustancia = NEW.f_sustancia AND f_espaciofisico = NEW.f_espaciofisico;
      RETURN NEW;

    END IF;

  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_bitacora_cantidad_update BEFORE INSERT OR UPDATE ON
t_bitacora FOR EACH ROW EXECUTE PROCEDURE update_cantidad_bitacora();
