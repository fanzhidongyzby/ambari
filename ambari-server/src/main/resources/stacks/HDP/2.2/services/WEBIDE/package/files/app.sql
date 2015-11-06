--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

--COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: webide
--
DROP SEQUENCE IF EXISTS file_id_seq CASCADE;
CREATE SEQUENCE file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.file_id_seq OWNER TO webide;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: hive_submit_time; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS hive_submit_time;
CREATE TABLE hive_submit_time (
    sessionid character varying,
    queryid character varying,
    starttime timestamp without time zone,
    endtime timestamp without time zone
);

ALTER TABLE public.hive_submit_time OWNER TO webide;

--
-- Name: mr_jar_id_seq; Type: SEQUENCE; Schema: public; Owner: webide
--
DROP SEQUENCE IF EXISTS mr_jar_id_seq CASCADE;
CREATE SEQUENCE mr_jar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.mr_jar_id_seq OWNER TO webide;

--
-- Name: mr_jar_file_info; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS mr_jar_file_info CASCADE;
CREATE TABLE mr_jar_file_info (
    file_id bigint DEFAULT nextval('mr_jar_id_seq'::regclass) NOT NULL,
    file_name character varying NOT NULL,
    owner character varying NOT NULL,
    qq_user character varying,
    state character varying DEFAULT 'normal'::character varying,
    create_time timestamp without time zone DEFAULT now(),
    last_modify_time timestamp without time zone DEFAULT now(),
    last_modify_user character varying,
    file_desc character varying,
    file_content bytea,
    file_type character varying DEFAULT 'jar'::character varying,
    last_deploy_time timestamp without time zone,
    deploy_state character varying DEFAULT 'undeployed'::character varying
);


ALTER TABLE public.mr_jar_file_info OWNER TO webide;

--
-- Name: mr_jar_file_modify_log; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS mr_jar_file_modify_log;
CREATE TABLE mr_jar_file_modify_log (
    file_id bigint,
    modify_time timestamp without time zone DEFAULT now(),
    modify_user character varying NOT NULL,
    log character varying NOT NULL
);

ALTER TABLE public.mr_jar_file_modify_log OWNER TO webide;

--
-- Name: sql_file_info; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS sql_file_info CASCADE;
CREATE TABLE sql_file_info (
    file_id bigint DEFAULT nextval('file_id_seq'::regclass) NOT NULL,
    file_name character varying NOT NULL,
    file_content character varying NOT NULL,
    create_time timestamp without time zone DEFAULT now(),
    last_modify_time timestamp without time zone,
    last_modify_user character varying,
    state character varying DEFAULT 'normal'::character varying,
    file_desc character varying,
    owner character varying,
    create_user character varying,
    qq_user character varying DEFAULT '281122610'::character varying
);


ALTER TABLE public.sql_file_info OWNER TO webide;

--
-- Name: sql_file_modify_log; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS sql_file_modify_log;
CREATE TABLE sql_file_modify_log (
    file_id bigint,
    modify_time timestamp without time zone DEFAULT now(),
    modify_user character varying NOT NULL,
    log character varying NOT NULL
);


ALTER TABLE public.sql_file_modify_log OWNER TO webide;

--
-- Name: sql_template; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS sql_template;
CREATE TABLE sql_template (
    file_name character varying NOT NULL,
    file_content character varying NOT NULL,
    create_time timestamp without time zone DEFAULT now(),
    file_desc character varying
);


ALTER TABLE public.sql_template OWNER TO webide;

--
-- Name: src_file_info; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS src_file_info;
CREATE TABLE src_file_info (
    file_id bigint DEFAULT nextval('file_id_seq'::regclass) NOT NULL,
    file_name character varying NOT NULL,
    file_type character varying,
    owner character varying NOT NULL,
    qq_user character varying,
    state character varying DEFAULT 'normal'::character varying,
    create_time timestamp without time zone DEFAULT now(),
    last_modify_time timestamp without time zone DEFAULT now(),
    last_modify_user character varying,
    file_desc character varying,
    file_content text,
    last_deploy_time timestamp without time zone,
    deploy_state character varying DEFAULT 'undeployed'::character varying
);


ALTER TABLE public.src_file_info OWNER TO webide;

--
-- Name: src_file_modify_log; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS src_file_modify_log;
CREATE TABLE src_file_modify_log (
    file_id bigint,
    modify_time timestamp without time zone DEFAULT now(),
    modify_user character varying NOT NULL,
    log character varying NOT NULL
);


ALTER TABLE public.src_file_modify_log OWNER TO webide;

--
-- Name: src_template; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS src_template;
CREATE TABLE src_template (
    file_name character varying NOT NULL,
    file_type character varying NOT NULL,
    file_content character varying NOT NULL,
    create_time timestamp without time zone DEFAULT now(),
    file_desc character varying
);


ALTER TABLE public.src_template OWNER TO webide;

--
-- Name: tdwuser; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS  tdwuser;
CREATE TABLE tdwuser (
    user_name character varying,
    passwd character varying
);


ALTER TABLE public.tdwuser OWNER TO webide;

insert into tdwuser values('thive', 'thive');

--
-- Name: template_guser_1; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS template_guser_1;
CREATE TABLE template_guser_1 (
    gqq_user character varying NOT NULL
);


ALTER TABLE public.template_guser_1 OWNER TO webide;

--
-- Name: webide_api_call_info; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS webide_api_call_info;
CREATE TABLE webide_api_call_info (
    gid character varying NOT NULL,
    uid character varying NOT NULL,
    method character varying NOT NULL,
    params character varying,
    call_result character varying,
    detail character varying,
    call_start_time timestamp without time zone DEFAULT now(),
    call_end_time timestamp without time zone DEFAULT now(),
    insert_time timestamp without time zone DEFAULT now(),
    ip character varying,
    port integer
);


ALTER TABLE public.webide_api_call_info OWNER TO webide;

--
-- Name: webide_sql_exe_info; Type: TABLE; Schema: public; Owner: webide; Tablespace: 
--
DROP TABLE IF EXISTS webide_sql_exe_info;
CREATE TABLE webide_sql_exe_info (
    session_id character varying NOT NULL,
    sql_id character varying NOT NULL,
    qq_user character varying NOT NULL,
    tdw_user character varying NOT NULL,
    sql character varying NOT NULL,
    start_time timestamp without time zone DEFAULT now(),
    end_time timestamp without time zone,
    process integer DEFAULT 0,
    ip character varying,
    port integer DEFAULT 8080,
    execute_state character varying NOT NULL,
    detail character varying,
    gqq_user character varying
);


ALTER TABLE public.webide_sql_exe_info OWNER TO webide;

--
-- Name: mr_jar_file_info_file_name_owner_key; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY mr_jar_file_info
    ADD CONSTRAINT mr_jar_file_info_file_name_owner_key UNIQUE (file_name, owner);


--
-- Name: mr_jar_file_info_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY mr_jar_file_info
    ADD CONSTRAINT mr_jar_file_info_pkey PRIMARY KEY (file_id);


--
-- Name: sql_file_info_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY sql_file_info
    ADD CONSTRAINT sql_file_info_pkey PRIMARY KEY (file_id);


--
-- Name: sql_template_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY sql_template
    ADD CONSTRAINT sql_template_pkey PRIMARY KEY (file_name);


--
-- Name: src_file_info_file_name_owner_key; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY src_file_info
    ADD CONSTRAINT src_file_info_file_name_owner_key UNIQUE (file_name, owner);


--
-- Name: src_file_info_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY src_file_info
    ADD CONSTRAINT src_file_info_pkey PRIMARY KEY (file_id);


--
-- Name: src_template_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY src_template
    ADD CONSTRAINT src_template_pkey PRIMARY KEY (file_name);


--
-- Name: template_guser_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY template_guser_1
    ADD CONSTRAINT template_guser_pkey PRIMARY KEY (gqq_user);


--
-- Name: webide_sql_exe_info_pkey; Type: CONSTRAINT; Schema: public; Owner: webide; Tablespace: 
--

ALTER TABLE ONLY webide_sql_exe_info
    ADD CONSTRAINT webide_sql_exe_info_pkey PRIMARY KEY (sql_id);


--
-- Name: start_time_index; Type: INDEX; Schema: public; Owner: webide; Tablespace: 
--

CREATE INDEX start_time_index ON webide_api_call_info USING btree (call_start_time);


--
-- Name: uid_gid_method_index; Type: INDEX; Schema: public; Owner: webide; Tablespace: 
--

CREATE INDEX uid_gid_method_index ON webide_api_call_info USING btree (uid, gid, method);


--
-- Name: mr_jar_file_modify_log_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: webide
--

ALTER TABLE ONLY mr_jar_file_modify_log
    ADD CONSTRAINT mr_jar_file_modify_log_file_id_fkey FOREIGN KEY (file_id) REFERENCES mr_jar_file_info(file_id) ON DELETE CASCADE;


--
-- Name: sql_file_modify_log_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: webide
--

ALTER TABLE ONLY sql_file_modify_log
    ADD CONSTRAINT sql_file_modify_log_file_id_fkey FOREIGN KEY (file_id) REFERENCES sql_file_info(file_id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: webide
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM webide;
GRANT ALL ON SCHEMA public TO webide;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

