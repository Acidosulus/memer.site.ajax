--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$600000$W2kP5Nnszi3tuqC5TKLO1q$pXJiOwJUdB/YZI3DapLbvLE++stdQCfOkjNG4DD4tak=	2024-04-24 23:37:12.809171+07	t	admin			acidos@yandex.ru	t	t	2023-09-06 09:22:10.864961+07
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2023-09-06 09:20:53.106721+07
2	auth	0001_initial	2023-09-06 09:20:53.538293+07
3	admin	0001_initial	2023-09-06 09:20:53.640278+07
4	admin	0002_logentry_remove_auto_add	2023-09-06 09:20:53.672609+07
5	admin	0003_logentry_add_action_flag_choices	2023-09-06 09:20:53.729274+07
6	contenttypes	0002_remove_content_type_name	2023-09-06 09:20:53.791837+07
7	auth	0002_alter_permission_name_max_length	2023-09-06 09:20:53.838848+07
8	auth	0003_alter_user_email_max_length	2023-09-06 09:20:53.888995+07
9	auth	0004_alter_user_username_opts	2023-09-06 09:20:53.942014+07
10	auth	0005_alter_user_last_login_null	2023-09-06 09:20:53.990061+07
11	auth	0006_require_contenttypes_0002	2023-09-06 09:20:54.041782+07
12	auth	0007_alter_validators_add_error_messages	2023-09-06 09:20:54.096699+07
13	auth	0008_alter_user_username_max_length	2023-09-06 09:20:54.153488+07
14	auth	0009_alter_user_last_name_max_length	2023-09-06 09:20:54.201597+07
15	auth	0010_alter_group_name_max_length	2023-09-06 09:20:54.272899+07
16	auth	0011_update_proxy_permissions	2023-09-06 09:20:54.312458+07
17	auth	0012_alter_user_first_name_max_length	2023-09-06 09:20:54.361114+07
18	sessions	0001_initial	2023-09-06 09:20:54.479664+07
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
y60u4bbiwxeu48914a8ndsby3ajz44sq	.eJxVjEsOAiEQBe_C2pDmJ8Gle89AummQUQPJfFYT764ks9BtVb23i4jbWuO25DlOLC5CidMvI0zP3IbgB7Z7l6m3dZ5IjkQedpG3zvl1Pdq_g4pL_a6dc6UUbSCQ0QqKNwxoHClPgQa3xJB90I44WUgZvLVnTVphCqSCeH8A06U3gw:1qdiCI:LKhkQ_aBySB-27OyTu2cw3Rzr6pDTa-HsJoIha_p-yo	2023-09-20 09:23:14.021543+07
3j4aziueat4df9cmh3fa0c0muyzo5rwa	.eJxVjEsOAiEQBe_C2pDmJ8Gle89AummQUQPJfFYT764ks9BtVb23i4jbWuO25DlOLC5CidMvI0zP3IbgB7Z7l6m3dZ5IjkQedpG3zvl1Pdq_g4pL_a6dc6UUbSCQ0QqKNwxoHClPgQa3xJB90I44WUgZvLVnTVphCqSCeH8A06U3gw:1qeWRt:lLKv-hfZwXiHeEZiu5gvnzHZpS3Rk0PynMx3Au2hOGE	2023-09-22 15:02:41.823634+07
aol3zzxgnioj3f2q7wyycts05opmfo7k	.eJxVjEsOAiEQBe_C2pDmJ8Gle89AummQUQPJfFYT764ks9BtVb23i4jbWuO25DlOLC5CidMvI0zP3IbgB7Z7l6m3dZ5IjkQedpG3zvl1Pdq_g4pL_a6dc6UUbSCQ0QqKNwxoHClPgQa3xJB90I44WUgZvLVnTVphCqSCeH8A06U3gw:1qnAhT:WlXHV8oi3KwOCepTnKemSdDTG2DkJYUz2olZJuAS3Ms	2023-10-16 11:38:31.548688+07
9cs82xhtxx07fcy2vgwyf23cgc77skk9	.eJxVjEsOAiEQBe_C2pDmJ8Gle89AummQUQPJfFYT764ks9BtVb23i4jbWuO25DlOLC5CidMvI0zP3IbgB7Z7l6m3dZ5IjkQedpG3zvl1Pdq_g4pL_a6dc6UUbSCQ0QqKNwxoHClPgQa3xJB90I44WUgZvLVnTVphCqSCeH8A06U3gw:1qtfwe:hIC1TIGMMwi9yRYupZFE3C2OzkTTeuDictz6Qxd8Vms	2023-11-03 10:13:04.811202+07
5ivjcfp395jfctrpnq59rtw2qfneuglg	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rirha:a89GtUqIuLssZP-v1WdrCbOVaHuK5b0LUDrZ68M8aqI	2024-03-23 15:05:06.939966+07
uf86m33rio1pt4xss47t44troolrl7al	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rirpi:i-ftOJi1X157t7MR1EJdd_uh7pU-0ZwzpxiJRVPM8EM	2024-03-23 15:13:30.3458+07
5jdpzvu37uq8sifiodcb39x7pw6zfriu	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rirq3:IYuxwHk-920wRdtXFn-tyqaxA23bzbEAdqTXYHbT_Gc	2024-03-23 15:13:51.076077+07
hqbu00kjissbs4ux8egi493gkpcxd9g3	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1riwsk:zPl9_aP0bITvVJ4E3ZWp8ZLvBHtr-lmkfebLo1G1ukM	2024-03-23 20:36:58.71602+07
ljfewfostts1bzwlymrtf8kfpiby7m60	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rjCB6:TtVq-q8vm996pk3jSkL6YQvMQMd0I0nGs8RUTThJrmg	2024-03-24 12:56:56.098387+07
pr4oxyvmbb9frvatbk0cpct89f5r3cre	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rjY6P:TXEyEiguNTR-wsNwlMvq2Yfj0jxJatZFBewLTU4YENA	2024-03-25 12:21:33.210688+07
bh8q34g1gcy9lau6bxqrofdsccerxgza	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rjthp:50LyRCIq-vHYD5yTMyYglM4r40EKARNiTazj-lFLyHs	2024-03-26 11:25:37.268506+07
qduiabkd4fxm3a9i58p7z8puliaj0qyf	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rkSE9:8vacXqBZKyO-dG0GIikXCzX-O0WbGaJXTPOz6fyuxt0	2024-03-28 00:17:17.175873+07
wzqw7s40as6k5qum1tnjivll7esotgwg	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rkSER:kb0WUQ2kUjWvkJKXbXYlVJhcMabUD04hq9nKvp_gOas	2024-03-28 00:17:35.306676+07
iluohh97ijc4e30i50hx6jmj8h4qw7m5	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rl9xu:obHX4EMtVolRiBnZmldiJF5Y6YKP45QU39qygXN37Hs	2024-03-29 22:59:26.631326+07
uyd6xshylflcnutl42cj1mz3r6clr6cm	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1roXjy:ImWycacTixGplPk7Ad68_seXGBW4WysGTAYy0NpKvAM	2024-04-08 06:59:02.276675+07
azjeolzwetd15alxvd39agft15t3phvh	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1royRV:QryBr1H7SwFHcgJ9Ln5D1Sv7vdXV0Xcdg_OIuJmNvzk	2024-04-09 11:29:45.753873+07
lu4n2i1i1c2fnpzyk87c6uyuzsdvr62g	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1royS1:z4p__ocVUogPk2Mu2Ahf9GraKK6j-lOQ6ZFp_IemAOA	2024-04-09 11:30:17.224176+07
38qqqteu9lebkc15t7qterasa9n9tf9l	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rpOMe:2xXkBII4odkNGpqmxVA2LKJ8DEvS4-dG2ipZckXLDjY	2024-04-10 15:10:28.603596+07
tr3ubapv6yp95ezgbmubzk4upg1abiwl	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rpf2N:kPB_4sQeLcvJboDGWNF164uUZUEMMKwV39jGbqIVewg	2024-04-11 08:58:39.380412+07
l2xfuozcifbfajujndhpxpie8en37kl5	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rqwUH:nP6v5MJM19sV2ArB_vauhgZLQRJg1utWBrIM1QRUDUA	2024-04-14 21:48:45.696777+07
juwrmeo1gs9dkemm2eab376agzocdneq	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rqwvx:Dwo5lLWLmGFaMFuMv1vRxI2KAV7OxqZkl7V_0t6whEU	2024-04-14 22:17:21.310743+07
j3f2vvwjn2akbi6x85znq6p6djraafbk	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rtg2M:uttlPmXQZHefxiu_yuBl_nPvstIjcHJ8Jg530m-omN8	2024-04-22 10:51:14.763333+07
z05teskmjzgnurrm61dnrf1mn9lj88z8	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rthEo:RlvuJBdDEJLrqqDXoL29nyeQzzlBJhzmZM_R5mzyBRU	2024-04-22 12:08:10.59289+07
v4t6gu71ggnbant1i4q8d44hkcy3z7nb	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1ru1eC:OPP9-oVLnhgjeQP-9Otehg4YgWUp0hBfVKBHmrF2c-c	2024-04-23 09:55:44.4965+07
br4yh91oeuor1e1yqgnh7bs8f6xebh0n	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1ru1lq:PYUJkal63PjRAwp5hsiI_xpvVwOQP9XaeEjUBanb8PA	2024-04-23 10:03:38.137931+07
gbktlfoys8d67ytla6tccwefddvr3903	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1ruamo:GXTZyzecYmPD_loMdD2eIoc68OmpFu15dXSzB9peqV0	2024-04-24 23:26:58.739427+07
vy79vw4v8nz9ie6a1l0t52zpgkdfs064	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rv7be:qwmUXd_y_YztI-o5G_kTTNP8xq0fVPa-tu30L8Dvsyk	2024-04-26 10:29:38.194645+07
solthsmqhb505unjs0bh4p9q88g11mpm	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rvBP9:JnRbta8lZtb6ZTfX8hcdPDXejPnf461PhxTYHQks1aU	2024-04-26 14:32:59.106761+07
rus31kxx4838iyews1dekddv4oufkwds	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rvsg8:gGmk4ZoSvuUcJJ2egON1_ofjAQ9P5WMVWq6-mv4brDU	2024-04-28 12:45:24.838209+07
3772d9h2glwvt03mgfgd76sppqu743vt	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rwAqL:7c726sbLdnKwYEvU6GQ6tG73rLF_znKFhyzcg4Afxtg	2024-04-29 08:09:09.06841+07
2r400ch338xu0llhb6tgyiwqtde7idcn	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rxRN2:rEM5HxnU_a0ItiTIQj2gqHrZj6IAHQFV-6il4yn3cYI	2024-05-02 20:00:08.572163+07
0a41asa8swoc3a4pca2swltlk445tiy9	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1ry13c:L7X6xqdskV2AaU2-t4TWDE8oPmB9qFh3QYUyMsIjqs4	2024-05-04 10:06:28.48065+07
xohunrn651gp2gyrgv0yzuy2pgwuc9xf	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rz47v:sUzSinzuHsqlF9WIFuXRYGwbnmSBOe1au6fDzFGSB0Y	2024-05-07 07:35:15.431407+07
4g746onc858z373vcmud6etxnpmtles2	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rzWG4:9C4dhN1C91tyFe8yldWzkBcu_aQ5U3NN8mt2s53fud8	2024-05-08 13:37:32.737857+07
kqesum85u7mcuf1zjn5fwez7czcdd9nj	.eJxVjMsOwiAQRf-FtSEMhJdL934DGYZRqoYmpV0Z_12adKHbc869b5FwW2vaOi9pKuIsQJx-WUZ6cttFeWC7z5Lmti5TlnsiD9vldS78uhzt30HFXscaozHRWx0RtGFSwQwQAAgCKAUZh-JCTntD_uYdRW0hMrkcVGGw4vMFqOo2sA:1rzfcO:T0O7kPqGNcsVsk8Dvo_RHJgHQHEcAet3UUK2cMf1woA	2024-05-08 23:37:12.814449+07
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 24, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 6, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 18, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

