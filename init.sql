CREATE USER tasks_queue CREATEDB LOGIN PASSWORD 'tasks_queue';
CREATE DATABASE tasks_queue WITH OWNER = tasks_queue CONNECTION LIMIT = -1;
GRANT ALL PRIVILEGES ON DATABASE tasks_queue to tasks_queue;