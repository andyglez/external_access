def get_words(word, lang='es'):
    wds = {
        'user': {
            'en' : 'User',
            'es' : 'Usuario',
            'ca' : 'Usuari'
        },
        'password': {
            'en' : 'Password',
            'es' : 'Contraseña',
            'ca' : 'Contrasenya'
        },
        'auth_title': {
            'en' : 'Log in',
            'es' : 'Autenticación',
            'ca' : 'Autenticació'
        },
        'unregistered': {
            'en' : 'Not registered yet?',
            'es' : 'No se ha registrado aún?',
            'ca' : 'No s\'ha registrat encara?'
        },
        'ask': {
            'en' : 'Ask registration',
            'es' : 'Pedir registro',
            'ca' : 'Demanar registro'
        },
        'dismiss': {
            'en' : 'Dismiss and go back',
            'es' : 'Descartar e ir atrás',
            'ca' : 'Descartar i anar arrera'
        },
        'name': {
            'en' : 'Name',
            'es' : 'Nombre',
            'ca' : 'Nom'
        },
        'last_name': {
            'en' : 'Last Name',
            'es' : 'Apellidos',
            'ca' : 'Cognom'
        },
        'phone': {
            'en' : 'Phone',
            'es' : 'Teléfono',
            'ca' : 'Teléfon'
        },
        'welcome': {
            'en' : 'Welcome',
            'es' : 'Bienvenido',
            'ca' : 'Benvingut'
        },
        'more_details' : {
            'en' : 'Show Details',
            'es' : 'Mostrar Detalles',
            'ca' : 'Mostrar Detalls'
        },
        'less_details' : {
            'en' : 'Less Details',
            'es' : 'Menos Detalles',
            'ca' : 'Menys Detalls'
        },
        'start' : {
            'en' : 'Start Time',
            'es' : 'Tiempo de Inicio',
            'ca' : 'Temps d\'inici'
        },
        'stop' : {
            'en' : 'Stop Time',
            'es' : 'Tiempo Final',
            'ca' : 'Temps de Final'
        },
        'consumed' : {
            'en' : 'Consumed',
            'es' : 'Consumido',
            'ca' : 'Consumit'
        },
        'enter' : {
            'en' : 'Enter',
            'es' : 'Entrar',
            'ca' : 'Entrar'
        },
        'language' : {
            'en' : 'Select your language',
            'es' : 'Escoja su idioma',
            'ca' : 'Tria la seva llengua'
        },
        'app_name' : {
            'en' : 'External Access',
            'es' : 'Acceso Telefónico',
            'ca' : 'Accés Telefònico'
        },
        'exit' : {
            'en' : 'Exit',
            'es' : 'Salir',
            'ca' : 'Sortir'
        },
        'quota' : {
            'en' : 'Quota',
            'es' : 'Cuota',
            'ca' : 'Quota'
        },
        'quota_consumed' : {
            'en' : 'Quota consumed',
            'es' : 'Consumo de la cuota',
            'ca' : 'Consum de la quota'
        },
        'remain' : {
            'en' : 'Remaining time',
            'es' : 'Tiempo restante',
            'ca' : 'Temps restant'
        },
        'profile': {
            'en' : 'See Profile',
            'es' : 'Ver Perfil',
            'ca' : 'Veure Perfil'
        },
        'home' : {
            'en' : 'Home',
            'es' : 'Inicio',
            'ca' : 'Inici'
        },
        'area' : {
            'en' : 'Area',
            'es' : 'Area',
            'ca' : 'Area'
        },
        'email' : {
            'en' : 'Email',
            'es' : 'Correo',
            'ca' : 'Correu'
        },
        'address' : {
            'en' : 'Address',
            'es' : 'Dirección',
            'ca' : 'Direcció'
        },
        'modify' : {
            'en' : 'Modify Password',
            'es' : 'Modificar Contraseña',
            'ca' : 'Modificar Contrasenya'
        },
        'new': {
            'en' : 'New',
            'es' : 'Nueva',
            'ca' : 'Nova'
        },
        'verify': {
            'en' : 'Verify',
            'es' : 'Verifique',
            'ca' : 'Verifiqui'
        },
        'search_by_name' : {
            'en' : 'Search by name',
            'es' : 'Buscar por nombre',
            'ca' : 'Buscar per nom'
        },
        'force' : {
            'en' : 'Force Elimination',
            'es' : 'Forzar Eliminación',
            'ca' : 'Forçar Eliminació'
        },
        'create' : {
            'en' : 'Create User',
            'es' : 'Crear Usuario',
            'ca' : 'Crear Usuari'
        },
        'pendings' : {
            'en' : 'See Pendings',
            'es' : 'Ver Pendientes',
            'ca' : 'Veure Arracades'
        },
        'no_results' : {
            'en' : 'No results were found',
            'es' : 'No se encontraron resultados',
            'ca' : 'No s\'han trobat resultats'
        },
        'notes' : {
            'en' : 'Notes',
            'es' : 'Notas',
            'ca' : 'Notes'
        },
        'group' : {
            'en' : 'Group',
            'es' : 'Grupo',
            'ca' : 'Grup'
        },
        'authorized' : {
            'en' : 'Authorized until',
            'es' : 'Autorizado hasta',
            'ca' : 'Autoritzat fins'
        },
        'change' : {
            'en' : 'Change Rol',
            'es' : 'Cambiar Rol',
            'ca' : 'Canviar Rol'
        }
    }
    return wds[word][lang]