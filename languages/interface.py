def get_words(word, lang='es'):
    wds = {
        'user': {
            'en' : 'User',
            'es' : 'Usuario',
            'ca' : 'Usuari'
        },
        'username': {
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
            'ca' : 'Adreça'
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
        'search' : {
            'en' : 'Search',
            'es' : 'Buscar',
            'ca' : 'Buscar'
        },
        'search_by' : {
            'en' : 'Search by',
            'es' : 'Buscar por',
            'ca' : 'Buscar per'
        },
        'force' : {
            'en' : 'Delete',
            'es' : 'Eliminar',
            'ca' : 'Eliminar'
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
            'en' : 'Change',
            'es' : 'Cambiar',
            'ca' : 'Canviar'
        },
        'results': {
            'en' : 'Showing results',
            'es' : 'Mostrando resultados',
            'ca' : 'Mostrant resultats'
        },
        'page' : {
            'en' : 'Page',
            'es' : 'Página',
            'ca' : 'Página'
        },
        'first' : {
            'en' : 'First',
            'es' : 'Primera',
            'ca' : 'Primera'
        },
        'prev' : {
            'en' : 'Previous',
            'es' : 'Anterior',
            'ca' : 'Anterior'
        },
        'next' : {
            'en' : 'Next',
            'es' : 'Siguiente',
            'ca' : 'Següent'
        },
        'last' : {
            'en' : 'Last',
            'es' : 'Ultima',
            'ca' : 'Postrera'
        },
        'bonus': {
            'en' : 'Add Bonus',
            'es' : 'Bonificar',
            'ca' : 'Bonificar'
        },
        'logs': {
            'en' : 'Logs',
            'es' : 'Registros',
            'ca' : 'Registres'
        },
        'general': {
            'en' : 'General Info',
            'es' : 'Información General',
            'ca' : 'Informació General'
        },
        'func'   : {
            'en' : 'Profile Functions',
            'es' : 'Funciones de Perfil',
            'ca' : 'Funcions de Perfil'
        },
        'func_star' :{
            'en' : 'Administration Functions',
            'es' : 'Funciones Administrativas',
            'ca' : 'Funcions Administratives'
        },
        'lost' : {
            'en' : 'Lost your password?',
            'es' : 'Ha perdido la contraseña?',
            'ca' : 'Ha perdut la contrasenya?'
        },
        'newpass':{
            'en' : 'Retrieve Password',
            'es' : 'Recuperar Contraseña',
            'ca' : 'Recuperar Contrasenya'
        },
        'bonus_time' : {
            'en' : 'Time (in hours)',
            'es' : 'Tiempo (en horas)',
            'ca' : 'Temps (en hores)'
        },
        'comment': {
            'en' : 'Comments',
            'es' : 'Comentarios',
            'ca' : 'Comentaris'
        },
        'expires': {
            'en' : 'Expiration Date',
            'es' : 'Fecha de Expiración',
            'ca' : 'Data d\'expiració'
        },
        'app_name': {
            'en' : 'Remote Access',
            'es' : 'Acceso Remoto',
            'ca' : 'Acces Remot'
        },
        'doc' : {
            'en' : 'Obtain Document',
            'es' : 'Obtener Documento',
            'ca' : 'Obtenir Document'
        },
        'authorize': {
            'en' : 'Authorize',
            'es' : 'Autorizar',
            'ca' : 'Autoritzar'
        },
        'id': {
            'en' : 'DNI',
            'es' : 'Carnet de Identidad',
            'ca' : 'DNI'
        },
        'notes' : {
            'en' : 'Petition Date',
            'es' : 'Fecha de Petición',
            'ca' : 'Data de Petició'
        }
    }
    return wds[word][lang]