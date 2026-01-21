CREATE DATABASE legacy_warehouse_db;

\c legacy_warehouse_db

CREATE TABLE old_items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    info TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO old_items (item_name, cost, info) VALUES
('Вінтажний програвач', 8500.00, 'Програвач вінілу з вбудованими динаміками'),
('Набір об''єктивів', 12300.50, 'Набір для мобільної фотографії'),
('Механічна клавіатура', 4200.00, 'RGB підсвітка, сині світчі'),
('Монітор 27 дюймів', 9800.00, 'IPS матриця, 144 Гц'),
('Ігрова миша', 1500.00, 'Оптичний сенсор 16000 DPI');

