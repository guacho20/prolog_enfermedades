abrir_conexion :-
    odbc_connect('PostgreSQL30',_,
		[user(postgres),
		password('postgres'),
		alias(postgresql),
		open(once)
		]).

es_enfermedad(A,X) :-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO diseases(name) VALUES (\'~w\')'-[A],
                affected(X)).

es_sintoma(A,X) :-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO symptoms(name) VALUES (\'~w\')'-[A],
                affected(X)).

enfermedades(X):-
    abrir_conexion,
    odbc_query('postgresql','SELECT id, name FROM diseases ORDER BY id DESC ', X). 

sintomas(X):-
    abrir_conexion,
    odbc_query('postgresql','SELECT id, name FROM symptoms', X). 

    