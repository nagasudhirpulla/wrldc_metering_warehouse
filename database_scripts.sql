-- https://www.covermymeds.com/main/insights/articles/on-update-timestamps-mysql-vs-postgres/
-- updated at functionality of meter_master_data table
CREATE FUNCTION update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
$$;

CREATE TRIGGER meter_master_data_updated_at_modtime BEFORE UPDATE ON meter_master_data FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

