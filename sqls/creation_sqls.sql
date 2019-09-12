-- Created on Wed Sep 11 13:20:43 2019

-- @author: Nagasudhir

-- postgresql data types - https://www.postgresql.org/docs/9.3/datatype-numeric.html

-- Table: public.raw_meter_data

-- DROP TABLE public.raw_meter_data;

CREATE TABLE public.raw_meter_data
(
    id integer NOT NULL DEFAULT nextval('raw_meter_data_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    meter_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    meter_wh real NOT NULL,
    freq_code integer NOT NULL,
    data_time timestamp without time zone NOT NULL,
    CONSTRAINT raw_meter_data_pkey PRIMARY KEY (id),
    CONSTRAINT meter_id_data_time_unique UNIQUE (meter_id, data_time)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.raw_meter_data
    OWNER to postgres;


-- Table: public.meter_master_data

-- DROP TABLE public.meter_master_data;

CREATE TABLE public.meter_master_data
(
    id integer NOT NULL DEFAULT nextval('meter_master_data_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    from_time timestamp without time zone NOT NULL,
    location_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    meter_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    ct_ratio real NOT NULL,
    pt_ratio real NOT NULL,
    description character varying(500) COLLATE pg_catalog."default",
    created_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status character varying(10) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT meter_master_data_pkey PRIMARY KEY (id),
    CONSTRAINT from_time_location_id_unique UNIQUE (from_time, location_id)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.meter_master_data
    OWNER to postgres;

-- Trigger: meter_master_data_updated_at_modtime

-- DROP TRIGGER meter_master_data_updated_at_modtime ON public.meter_master_data;

CREATE TRIGGER meter_master_data_updated_at_modtime
    BEFORE UPDATE 
    ON public.meter_master_data
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_updated_at_column();



-- Table: public.raw_meter_cum_data

-- DROP TABLE public.raw_meter_cum_data;

CREATE TABLE public.raw_meter_cum_data
(
    id integer NOT NULL DEFAULT nextval('raw_meter_cum_data_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    data_time timestamp without time zone NOT NULL,
    meter_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cumm_active_energy_wh real NOT NULL,
    cumm_reactive_energy_high_wh real NOT NULL,
    cumm_reactive_energy_low_wh real NOT NULL,
    CONSTRAINT raw_meter_cum_data_pkey PRIMARY KEY (id),
    CONSTRAINT data_time_meter_id_unique UNIQUE (data_time, meter_id)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.raw_meter_cum_data
    OWNER to postgres;



-- Table: public.fict_master_data

-- DROP TABLE public.fict_master_data;

CREATE TABLE public.fict_master_data
(
    id integer NOT NULL DEFAULT nextval('fict_master_data_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    from_time timestamp without time zone NOT NULL,
    location_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    loc_formula character varying(500) COLLATE pg_catalog."default" NOT NULL,
    loc_name character varying(100) COLLATE pg_catalog."default",
    description character varying(500) COLLATE pg_catalog."default",
    created_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fict_master_data_pkey PRIMARY KEY (id),
    CONSTRAINT fict_master_from_time_location_id_unique UNIQUE (from_time, location_id)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.fict_master_data
    OWNER to postgres;

-- Trigger: fict_master_data_updated_at_modtime

-- DROP TRIGGER fict_master_data_updated_at_modtime ON public.fict_master_data;

CREATE TRIGGER fict_master_data_updated_at_modtime
    BEFORE UPDATE 
    ON public.fict_master_data
    FOR EACH ROW
    EXECUTE PROCEDURE public.update_updated_at_column();