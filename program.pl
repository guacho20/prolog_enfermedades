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

tiene_sintoma(A,B,X):-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO disease_symptoms(disease_id,symptom_id) VALUES (\'~w\',\'~w\')'-[A,B],
                affected(X)).

tiene_tratamiento(A,B,X):-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO treatments(disease_id, name) VALUES (\'~w\',\'~w\')'-[A,B],
                affected(X)).

enfermedades(X):-
    abrir_conexion,
    odbc_query('postgresql','SELECT id, name FROM diseases ORDER BY id DESC ', X). 

sintomas(X):-
    abrir_conexion,
    odbc_query('postgresql','SELECT id, name FROM symptoms', X). 

enfermedad_sintomas(X):-
    abrir_conexion,
    odbc_query('postgresql','select a.id, b.name as enfermedad,c.name as sintoma 
                from disease_symptoms a
                join diseases b on a.disease_id = b.id
                join symptoms c on a.symptom_id = c.id', X).

tratamientos(X):-
    abrir_conexion,
    odbc_query('postgresql','select a.id,b.name as enfermedad,a.name as tratamiento 
                from treatments a 
                join diseases b on a.disease_id = b.id', X).


                