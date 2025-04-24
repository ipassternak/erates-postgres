start:
 	uvicorn app.main:app
start-dev:
	uvicorn app.main:app --reload
create-admin-user:
	python -m app.cmd.create_admin_user