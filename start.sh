#!/bin/sh
cd "M1 zomato/backend"
exec gunicorn server:app --bind 0.0.0.0:${PORT:-5000}
