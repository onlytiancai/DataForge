# DataForge
DataForge: Build better insights from your data.

Manage and maintain data in MySQL, including backups, restores, imports, exports, and synchronizing data to ClickHouse or ES to make it easier to use.

## Roadmap

- MySQL Data Source Management.
- Make a UI for `util.export_table` of `mysqlsh`. 
- Make a UI for `util.import_table` of `mysqlsh`. 
- Make a UI for `util.dump_instance()`,`util.dump_schemas()`, `util.dump_tables` of `mysqlsh`. 
- Make a UI for `util.load_dump` of `mysqlsh`. 
- Make a UI for `util.copy_instance`, `util.copy_schemas`, `util.copy_tables` of `mysqlsh`. 
- CPU, memory, swap, disk io, network monitoring during task execution.
- Full, incremental database backup to disk or s3.
- Full, incremental backup of the specified table from disk or s3.
- Restore the specified table to the specified point in time.
- Full and incremental synchronization of specified tables to Clickhouse.
- Full and incremental synchronization of specified tables to Elasticsearch.
- Schedule data task.

## run

    celery -A celery_app worker --loglevel=info
    uvicorn main:app --reload
    
    cd vue-vben-admin
    pnpm run dev:antd

## pip install

prod

    python-multipart
    passlib
    pyjwt
    pydantic_settings
    tortoise-orm[asyncmy]
    tortoise-orm
    bcrypt

dev
    pytest
    httpx
