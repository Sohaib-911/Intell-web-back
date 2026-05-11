-- ============================================================
-- Intellisense Website — Supabase Database Schema
-- Generated from: app/schemas/* and app/routes/*
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- ── Enable UUID extension ────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ============================================================
-- 1. SERVICES
--    Used by: GET /api/services, GET /api/services/{slug}
--    Table:   services
-- ============================================================
CREATE TABLE IF NOT EXISTS services (
    id            UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug          TEXT        NOT NULL UNIQUE,
    title         TEXT        NOT NULL,
    short_description TEXT    NOT NULL,
    icon          TEXT,
    sort_order    INT         NOT NULL DEFAULT 0,
    full_description TEXT,
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_services_slug       ON services (slug);
CREATE INDEX IF NOT EXISTS idx_services_is_active  ON services (is_active);
CREATE INDEX IF NOT EXISTS idx_services_sort_order ON services (sort_order);


-- ============================================================
-- 2. PRODUCTS
--    Used by: GET /api/products, GET /api/products/{slug}
--    Table:   products
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
    id          UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug        TEXT        NOT NULL UNIQUE,
    name        TEXT        NOT NULL,
    tagline     TEXT,
    description TEXT,
    features    TEXT[],                   -- stored as a Postgres array
    image_url   TEXT,
    is_featured BOOLEAN     NOT NULL DEFAULT FALSE,
    demo_url    TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_slug        ON products (slug);
CREATE INDEX IF NOT EXISTS idx_products_is_featured ON products (is_featured);


-- ============================================================
-- 3. INDUSTRIES
--    Used by: GET /api/industries, GET /api/industries/{slug}
--    Table:   industries
-- ============================================================
CREATE TABLE IF NOT EXISTS industries (
    id          UUID    PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug        TEXT    NOT NULL UNIQUE,
    title       TEXT    NOT NULL,
    description TEXT,
    challenges  TEXT[],    -- list[str]
    solutions   TEXT[]     -- list[str]
);

CREATE INDEX IF NOT EXISTS idx_industries_slug ON industries (slug);


-- ============================================================
-- 4. BLOGS
--    Used by: GET /api/blogs, GET /api/blogs/{slug}
--    Table:   blogs
--    Note:    Routes filter on status = 'published'
-- ============================================================
CREATE TABLE IF NOT EXISTS blogs (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            TEXT        NOT NULL UNIQUE,
    title           TEXT        NOT NULL,
    excerpt         TEXT,
    cover_image_url TEXT,
    category        TEXT,
    tags            TEXT[],
    author_name     TEXT        NOT NULL DEFAULT 'Intellisense Team',
    content         TEXT        NOT NULL,
    status          TEXT        NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'published', 'archived')),
    published_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_blogs_slug         ON blogs (slug);
CREATE INDEX IF NOT EXISTS idx_blogs_status       ON blogs (status);
CREATE INDEX IF NOT EXISTS idx_blogs_published_at ON blogs (published_at DESC);


-- ============================================================
-- 5. TESTIMONIALS
--    Used by: GET /api/testimonials
--    Table:   testimonials
-- ============================================================
CREATE TABLE IF NOT EXISTS testimonials (
    id           UUID    PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_name  TEXT    NOT NULL,
    client_role  TEXT,
    company_name TEXT,
    quote        TEXT    NOT NULL,
    rating       INT     CHECK (rating BETWEEN 1 AND 5),
    image_url    TEXT,
    is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_testimonials_is_active ON testimonials (is_active);


-- ============================================================
-- 6. CUSTOMERS
--    Used by: GET /api/customers
--    Table:   customers
-- ============================================================
CREATE TABLE IF NOT EXISTS customers (
    id          UUID    PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        TEXT    NOT NULL,
    logo_url    TEXT,
    website_url TEXT,
    industry    TEXT,
    is_featured BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_customers_is_featured ON customers (is_featured);


-- ============================================================
-- 7. CASE STUDIES
--    Used by: GET /api/case-studies, GET /api/case-studies/{slug}
--    Table:   case_studies
--    Note:    Routes filter on status = 'published'
--             results is a free-form JSON object
-- ============================================================
CREATE TABLE IF NOT EXISTS case_studies (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            TEXT        NOT NULL UNIQUE,
    client_name     TEXT        NOT NULL,
    industry        TEXT,
    challenge       TEXT,
    cover_image_url TEXT,
    solution        TEXT,
    results         JSONB,                  -- dict[str, Any]
    testimonial_id  UUID        REFERENCES testimonials (id) ON DELETE SET NULL,
    status          TEXT        NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'published', 'archived')),
    published_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_case_studies_slug         ON case_studies (slug);
CREATE INDEX IF NOT EXISTS idx_case_studies_status       ON case_studies (status);
CREATE INDEX IF NOT EXISTS idx_case_studies_published_at ON case_studies (published_at DESC);


-- ============================================================
-- 8. CONTACT SUBMISSIONS
--    Used by: POST /api/contact
--    Table:   contact_submissions
--    Note:    source defaults to 'website', status defaults to 'new'
-- ============================================================
CREATE TABLE IF NOT EXISTS contact_submissions (
    id               UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    name             TEXT        NOT NULL,
    company          TEXT,
    email            TEXT        NOT NULL,
    phone            TEXT,
    service_interest TEXT,
    message          TEXT        NOT NULL,
    source           TEXT        NOT NULL DEFAULT 'website',
    status           TEXT        NOT NULL DEFAULT 'new'
                                 CHECK (status IN ('new', 'in_progress', 'resolved', 'spam')),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contact_status     ON contact_submissions (status);
CREATE INDEX IF NOT EXISTS idx_contact_email      ON contact_submissions (email);
CREATE INDEX IF NOT EXISTS idx_contact_created_at ON contact_submissions (created_at DESC);


-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- Enable RLS on all tables. The backend uses the service-role
-- key (bypasses RLS), so public anon access is locked down.
-- ============================================================

ALTER TABLE services            ENABLE ROW LEVEL SECURITY;
ALTER TABLE products            ENABLE ROW LEVEL SECURITY;
ALTER TABLE industries          ENABLE ROW LEVEL SECURITY;
ALTER TABLE blogs               ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonials        ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers           ENABLE ROW LEVEL SECURITY;
ALTER TABLE case_studies        ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_submissions ENABLE ROW LEVEL SECURITY;

-- Public read policies (anon role can SELECT published/active rows)
CREATE POLICY "Public can read active services"
    ON services FOR SELECT USING (is_active = TRUE);

CREATE POLICY "Public can read all products"
    ON products FOR SELECT USING (TRUE);

CREATE POLICY "Public can read all industries"
    ON industries FOR SELECT USING (TRUE);

CREATE POLICY "Public can read published blogs"
    ON blogs FOR SELECT USING (status = 'published');

CREATE POLICY "Public can read active testimonials"
    ON testimonials FOR SELECT USING (is_active = TRUE);

CREATE POLICY "Public can read featured customers"
    ON customers FOR SELECT USING (TRUE);

CREATE POLICY "Public can read published case studies"
    ON case_studies FOR SELECT USING (status = 'published');

-- contact_submissions: no public read; service-role only
-- (no SELECT policy means anon cannot read submissions)


-- ============================================================
-- SAMPLE SEED DATA  (optional — remove before production)
-- ============================================================

-- Sample service
INSERT INTO services (slug, title, short_description, icon, sort_order, full_description)
VALUES (
    'ai-solutions',
    'AI Solutions',
    'Cutting-edge artificial intelligence solutions tailored for enterprise.',
    'brain',
    1,
    'We design and deploy custom AI models, automation pipelines, and intelligent analytics platforms that drive measurable business outcomes.'
) ON CONFLICT (slug) DO NOTHING;

-- Sample product
INSERT INTO products (slug, name, tagline, description, features, is_featured)
VALUES (
    'intellisense-core',
    'Intellisense Core',
    'The intelligence layer for your business.',
    'A unified platform for AI-powered insights and automation.',
    ARRAY['Real-time analytics', 'No-code workflow builder', 'API-first architecture'],
    TRUE
) ON CONFLICT (slug) DO NOTHING;

-- Sample testimonial
INSERT INTO testimonials (client_name, client_role, company_name, quote, rating, is_active)
VALUES (
    'Sarah Johnson',
    'CTO',
    'Acme Corp',
    'Intellisense transformed how we handle data. The ROI was visible within the first quarter.',
    5,
    TRUE
);

-- Sample blog post
INSERT INTO blogs (slug, title, excerpt, author_name, content, status, published_at)
VALUES (
    'getting-started-with-ai',
    'Getting Started with AI in Your Business',
    'A practical guide to adopting AI without disrupting your operations.',
    'Intellisense Team',
    'Full content goes here...',
    'published',
    NOW()
) ON CONFLICT (slug) DO NOTHING;
