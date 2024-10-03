backend:
	fastapi dev ./backend/main.py

frontend:
	streamlit run ./frontend/home.py

run: backend frontend
	fastapi dev ./backend/main.py && streamlit run ./frontend/home.py 