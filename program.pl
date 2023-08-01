abrir_conexion :-
    odbc_connect('PostgreSQL30',_,
		[user(postgres),
		password('postgres'),
		alias(postgresql),
		open(once)
		]).

es_enfermedad(A,B) :-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO diseases(name, treatment) VALUES (\'~w\',\'~w\')'-[A,B]).

es_sintoma(A) :-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO symptoms(name) VALUES (\'~w\')'-[A]).

tiene_sintoma(A,B,X):-
    abrir_conexion,
    odbc_query('postgresql',
                'INSERT INTO disease_symptoms(disease_id,symptom_id) VALUES (\'~w\',\'~w\')'-[A,B],
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


diagnosticar(A,X):-
    abrir_conexion,
    odbc_query('postgresql','select enfermedad,tratamiento from (
        select count(symptom_id), disease_id,name as enfermedad,
            treatment as tratamiento
        from disease_symptoms a
        join diseases b on a.disease_id = b.id
        where symptom_id = ANY(string_to_array(?, ', ')::INTEGER[])
        group by disease_id,name,treatment
        ) a where count > 1'-[A],X).

diagnosticar2(A,X):-
    abrir_conexion,
    odbc_query('postgresql',A,X).