# MatchIT

Aplikacja jest napisana w Pythonie, używając frameworku Django.

## Docker

Najprościej uruchomić aplikację w Dockerze, używając polecenia:

	docker-compose up

W razie braku docker-compose'a można też użyć:

	docker build -t autism .
	docker run -p 8080:8080 autism

## Ręczne uruchamianie

W razie braku możliwości skorzystania z Dockera można przeprowadzić czynności ręcznie.

Poleca się pracować w wirtualnym środowisku Pythona. Wymagany jest sensownie współczesny Python 3.

	pip install -r requirements.txt
	./manage.py migrate
	./manage.py loaddata test/fixtures/data.json
	./manage.py runserver 8080

## Użycie

Strona będzie dostępna pod adresem localhost:8080.

Na stronie wyszukiwania możemy wyszukiwać nazwy miejsc, które chcemy znaleźć.

Dla wgranych testowych danych polecam wyszukać słowa "restauracja" lub "bar".

Oglądać oceny można, pozostając anonimowym użytkownikiem. Aby moć samemu oceniać, należy się zalogować jako test:test.
