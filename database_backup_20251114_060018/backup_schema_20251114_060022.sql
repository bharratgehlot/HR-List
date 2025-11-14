-- Database Schema Backup
-- Generated on: 2025-11-14 06:00:22.055585

CREATE TABLE IF NOT EXISTS contacts (
    id integer NOT NULL DEFAULT nextval('contacts_id_seq'::regclass),
    photo character varying(500),
    name character varying(255) NOT NULL,
    company character varying(255) NOT NULL,
    location character varying(255) NOT NULL,
    position character varying(255),
    number character varying(20) NOT NULL,
    email character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    url character varying(500),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

