backend:
	fastapi dev ./backend/main.py

frontend:
	python -m streamlit run ./frontend/home.py