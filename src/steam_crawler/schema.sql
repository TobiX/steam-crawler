CREATE TABLE IF NOT EXISTS apps_changes (
  appid INTEGER PRIMARY KEY,
  sha TEXT NOT NULL,
  size INTEGER NOT NULL,
  last_change_number INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS apps_changes_number ON apps_changes(last_change_number);

CREATE TABLE IF NOT EXISTS apps (
  appid INTEGER PRIMARY KEY,
  name TEXT,
  type TEXT,
  parent INTEGER,
  releasestate TEXT,
  os_windows INTEGER,
  os_macos INTEGER,
  os_linux INTEGER,
  osarch INTEGER,
  osextended TEXT,
  logo TEXT,
  logo_small TEXT,
  icon TEXT,
  clienttga TEXT,
  clienticon TEXT,
  has_adult_content INTEGER,
  has_adult_content_violence INTEGER,
  metacritic_name TEXT,
  controller_support TEXT,
  store_asset_mtime INTEGER,
  primary_genre INTEGER,
  steam_release_date INTEGER,
  community_visible_stats INTEGER,
  workshop_visible INTEGER,
  community_hub_visible INTEGER,
  exfgls INTEGER,
  review_score REAL,
  review_percentage INTEGER,
  developer TEXT,
  publisher TEXT,
  homepage TEXT,
  isfreeapp INTEGER,
  contenttype INTEGER,
  installdir TEXT,
  uselaunchcommandline INTEGER,
  steamcontrollertemplateindex INTEGER,
  steamconfigurator3rdpartynative INTEGER,
  last_change_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS steamdeck_category (
  category INTEGER PRIMARY KEY,
  status TEXT
);

INSERT INTO steamdeck_category (category, status) VALUES
  (1, 'Unsupported'),
  (2, 'Playable'),
  (3, 'Verified')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS apps_steamdeck (
  appid INTEGER PRIMARY KEY,
  category INTEGER,
  test_timestamp INTEGER,
  tested_build_id INTEGER,
  supported_input TEXT,
  requires_manual_keyboard_invoke INTEGER,
  requires_non_controller_launcher_nav INTEGER,
  primary_player_is_controller_slot_0 INTEGER,
  non_deck_display_glyphs INTEGER,
  small_text INTEGER,
  requires_internet_for_setup INTEGER,
  requires_internet_for_singleplayer INTEGER,
  recommended_runtime TEXT,
  requires_h264 INTEGER,
  last_change_number INTEGER NOT NULL,
  FOREIGN KEY(category) REFERENCES steamdeck_category(category)
);
