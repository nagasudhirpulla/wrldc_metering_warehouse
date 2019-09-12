--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

-- Started on 2019-09-12 15:10:26

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 202 (class 1255 OID 26068)
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 199 (class 1259 OID 26055)
-- Name: meter_master_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meter_master_data (
    id integer NOT NULL,
    from_time timestamp without time zone NOT NULL,
    location_id character varying(100) NOT NULL,
    meter_id character varying(100) NOT NULL,
    ct_ratio real NOT NULL,
    pt_ratio real NOT NULL,
    description character varying(500),
    created_at time without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status character varying(10) NOT NULL
);


ALTER TABLE public.meter_master_data OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 26053)
-- Name: meter_master_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meter_master_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_master_data_id_seq OWNER TO postgres;

--
-- TOC entry 2843 (class 0 OID 0)
-- Dependencies: 198
-- Name: meter_master_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meter_master_data_id_seq OWNED BY public.meter_master_data.id;


--
-- TOC entry 201 (class 1259 OID 26072)
-- Name: raw_meter_cum_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_meter_cum_data (
    id integer NOT NULL,
    data_time timestamp without time zone NOT NULL,
    meter_id character varying(100) NOT NULL,
    cumm_active_energy_wh real NOT NULL,
    cumm_reactive_energy_high_wh real NOT NULL,
    cumm_reactive_energy_low_wh real NOT NULL
);


ALTER TABLE public.raw_meter_cum_data OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 26070)
-- Name: raw_meter_cum_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.raw_meter_cum_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.raw_meter_cum_data_id_seq OWNER TO postgres;

--
-- TOC entry 2844 (class 0 OID 0)
-- Dependencies: 200
-- Name: raw_meter_cum_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.raw_meter_cum_data_id_seq OWNED BY public.raw_meter_cum_data.id;


--
-- TOC entry 197 (class 1259 OID 26045)
-- Name: raw_meter_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_meter_data (
    id integer NOT NULL,
    meter_id character varying(100) NOT NULL,
    act_en_wh real NOT NULL,
    freq_code integer NOT NULL,
    data_time timestamp without time zone NOT NULL
);


ALTER TABLE public.raw_meter_data OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 26043)
-- Name: raw_meter_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.raw_meter_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.raw_meter_data_id_seq OWNER TO postgres;

--
-- TOC entry 2845 (class 0 OID 0)
-- Dependencies: 196
-- Name: raw_meter_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.raw_meter_data_id_seq OWNED BY public.raw_meter_data.id;


--
-- TOC entry 2700 (class 2604 OID 26058)
-- Name: meter_master_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meter_master_data ALTER COLUMN id SET DEFAULT nextval('public.meter_master_data_id_seq'::regclass);


--
-- TOC entry 2703 (class 2604 OID 26075)
-- Name: raw_meter_cum_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_cum_data ALTER COLUMN id SET DEFAULT nextval('public.raw_meter_cum_data_id_seq'::regclass);


--
-- TOC entry 2699 (class 2604 OID 26048)
-- Name: raw_meter_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_data ALTER COLUMN id SET DEFAULT nextval('public.raw_meter_data_id_seq'::regclass);


--
-- TOC entry 2713 (class 2606 OID 26079)
-- Name: raw_meter_cum_data data_time_meter_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_cum_data
    ADD CONSTRAINT data_time_meter_id_unique UNIQUE (data_time, meter_id);


--
-- TOC entry 2709 (class 2606 OID 26067)
-- Name: meter_master_data from_time_location_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meter_master_data
    ADD CONSTRAINT from_time_location_id_unique UNIQUE (from_time, location_id);


--
-- TOC entry 2705 (class 2606 OID 26052)
-- Name: raw_meter_data meter_id_data_time_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_data
    ADD CONSTRAINT meter_id_data_time_unique UNIQUE (meter_id, data_time);


--
-- TOC entry 2711 (class 2606 OID 26065)
-- Name: meter_master_data meter_master_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meter_master_data
    ADD CONSTRAINT meter_master_data_pkey PRIMARY KEY (id);


--
-- TOC entry 2715 (class 2606 OID 26077)
-- Name: raw_meter_cum_data raw_meter_cum_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_cum_data
    ADD CONSTRAINT raw_meter_cum_data_pkey PRIMARY KEY (id);


--
-- TOC entry 2707 (class 2606 OID 26050)
-- Name: raw_meter_data raw_meter_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_meter_data
    ADD CONSTRAINT raw_meter_data_pkey PRIMARY KEY (id);


--
-- TOC entry 2716 (class 2620 OID 26069)
-- Name: meter_master_data meter_master_data_updated_at_modtime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER meter_master_data_updated_at_modtime BEFORE UPDATE ON public.meter_master_data FOR EACH ROW EXECUTE PROCEDURE public.update_updated_at_column();


-- Completed on 2019-09-12 15:10:27

--
-- PostgreSQL database dump complete
--