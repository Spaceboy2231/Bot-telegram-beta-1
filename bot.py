importar sistema operativo
importar asyncio
importar explotación florestal
importar re
de mecanografía importar Diccionario,Opcional,Tupla
importar tiempo
de enhebrado importar Hilo
importar sistema
importar json
importar códecs
importar solicitudes
importar html
de matraz importar Matraz
de telegrama importar Actualizar
de telegrama.extensión importar(
    Generador de aplicaciones,
    Controlador de comandos,
    Controlador de mensajes,
    filtros,
    Tipos de contexto,
)

TOKEN_BOT = sistema operativo.reinar.conseguir("BOT_TOKEN")
PUERTO = entero(sistema operativo.reinar.conseguir("PUERTO",10000))

explotación florestal.Configuración básica(
    formato="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    nivel=explotación florestal.INFORMACIÓN,
)
leñador = explotación florestal.obtener registrador(__nombre__)

app_flask = Matraz(__nombre__)
solicitud = Ninguno

TEXTO DE INICIO =(
    "👋 Bot de verificación de cookies de Netflix\norte\norte"
    "Pega aquí tus cookies de Netflix."\norte\norte"
    Formatos aceptados:\norte"
    "• Línea de encabezado `Cookie:` completa\norte"
    "• Formato Netscape: delimitado por tabulaciones o espacios"\norte"
    "• Formato de matriz JSON\norte"
    "• Pares clave=valor: NetflixId=...; SecureNetflixId=...; nfvdid=...\norte\norte"
    "Enviar cookies ahora:\norte\norte"
    "Bot de @ritsurex 🦖"
)

TEXTO DE AYUDA =(
    "Cómo funciona:\norte"
    "• Usa /start y luego pega las cookies.\norte"
    "• El bot valida las cookies mediante la API de Netflix."\norte"
    "• Si es válido, el bot lo convierte en un enlace de inicio de sesión (teléfono | PC | TV)"
)

# Todos los nombres de cookies reconocidos de Netflix
NOMBRES DE COOKIES DE NETFLIX ={
    'netflixid','securenetflixid','netflixcookies','__cookies-seguras-de-netflix',
    'nfvdid','flwssn','OptanonConsent','dsca','memclid','perfilesNuevaSesión',
    'cL','netflix-sans-normal-3-loaded','netflix-sin-negrita-3-cargado',
    'pas','OptanonAlertBoxClosed','hasVistoCookieDisclosure'
}

NOMBRE_DE_LA_COOKIE_RE = re.compilar(
    r"(?i)\b(netflixid|securenetflixid|netflixcookies|__secure-netflixcookies|"
    r"nfvdid|flwssn|OptanonConsent|dsca|memclid|profilesNewSession|cL|"
    r"netflix-sans-normal-3-loaded|netflix-sans-bold-3-loaded|pas|"
    r"OptanonAlertBoxClosed|hasSeenCookieDisclosure)\b"
)
COOKIE_KV_RE = re.compilar(r"^\s*([A-Za-z0-9_\\-]+)\s*=\s*(.+?)\s*$",re.DOTALL)


definición _is_json_cookie(texto:str)-> booleano:
    """Comprueba si el texto es un array de cookies JSON."""
    texto = texto.banda()
    si no(texto.empieza con('[')y texto.termina con(']'):
        devolver FALSO
    intentar:
        json.cargas(texto)
        devolver Verdadero
    excepto:
        devolver FALSO

definición _is_netscape_cookie(texto:str)-> booleano:
    """Comprueba si el texto está en formato de cookie de Netscape (separado por tabulaciones o espacios)."""
    pauta = texto.banda().dividir('\norte')
    si Len(pauta)< 1:
        devolver FALSO
    
    para línea en pauta:
        línea = línea.banda()
        si no línea o línea.empieza con('#'):
            continuar
        
        # Prueba primero con delimitadores de tabulación
        si '\t' en línea:
            regiones = línea.dividir('\t')
            si Len(regiones)>= 7:
                leñador.depurar(f"Formato de cookie de Netscape delimitado por tabulaciones detectado")
                devolver Verdadero
        demás:
            # Prueba con delimitadores de espacios (análisis más flexible)
            regiones = línea.dividir()
            si Len(regiones)>= 7:
                # Validar que tenga el formato de Netscape
                # Formato: ruta de bandera de dominio nombre de caducidad seguro valor
                dominio = regiones[0]
                bandera = regiones[1]
                camino = regiones[2]
                seguro = regiones[3]
                intentar:
                    vencimiento = entero(regiones[4])
                    nombre = regiones[5]
                    # Todo lo que sigue al nombre es el valor
                    si dominio.empieza con('.')y bandera en['VERDADERO','FALSO']y camino == '/' y seguro en['VERDADERO','FALSO']:
                        leñador.depurar(f"Formato de cookie de Netscape delimitado por espacios detectado")
                        devolver Verdadero
                excepto(Error de valor,Error de índice):
                    continuar
    
    devolver FALSO


definición _parece_encabezado_de_cookie(texto:str)-> booleano:
    t = texto.banda().más bajo()
    devolver t.empieza con("galleta:")o(";" en texto y "=" en texto)


definición _extraer_cookies_json(json_str:str)-> Diccionario[str,str]:
    "Extraer cookies del formato de matriz JSON."
    intentar:
        matriz_de_cookies = json.cargas(json_str)
        kV:Diccionario[str,str]={}
        
        si es instancia(matriz_de_cookies,lista):
            para objeto_de_cookies en matriz_de_cookies:
                si es instancia(objeto_de_cookies,diccionario):
                    nombre = objeto_de_cookies.conseguir('nombre','')
                    valor = objeto_de_cookies.conseguir('valor','')
                    si nombre y valor:
                        kV[nombre]= valor
        devolver kV
    excepto Excepción como mi:
        leñador.error(f"Error al analizar las cookies JSON:{mi}")
        devolver{}


definición _extraer_cookies_netscape(netscape_str:str)-> Diccionario[str,str]:
    """Extrae las cookies del formato Netscape (admite tanto el delimitado por tabulaciones como por espacios)."""
    kV:Diccionario[str,str]={}
    pauta = netscape_str.banda().dividir('\norte')
    
    para línea en pauta:
        línea_original = línea
        línea = línea.banda()
        
        si no línea o línea.empieza con('#'):
            continuar
        
        # Determinar el delimitador (tabulador o espacio)
        si '\t' en línea:
            # Formato delimitado por tabulaciones
            regiones = línea.dividir('\t')
            delimitador = '\t'
        demás:
            # Formato delimitado por espacios (más complejo)
            regiones = línea.dividir()
            delimitador = ' '
        
        si Len(regiones)>= 7:
            intentar:
                si delimitador == '\t':
                    # Formato de tabulación: dominio bandera ruta caducidad segura nombre valor
                    dominio = regiones[0]
                    bandera = regiones[1]
                    camino = regiones[2]
                    seguro = regiones[3]
                    vencimiento = regiones[4]
                    nombre = regiones[5]
                    valor = regiones[6]
                demás:
                    # Formato de espacio: dominio bandera ruta caducidad segura nombre valor...
                    dominio = regiones[0]
                    bandera = regiones[1]
                    camino = regiones[2]
                    seguro = regiones[3]
                    intentar:
                        vencimiento = entero(regiones[4])
                    excepto Error de valor:
                        continuar
                    nombre = regiones[5]
                    # Todo lo que sigue a la posición 6 forma parte del valor (para valores delimitados por espacios).
                    # Reconstruir el valor de la línea original
                    # Formato: ruta de bandera de dominio nombre de caducidad seguro valor
                    fósforo = re.fósforo(
                        r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)$',
                        línea
                    )
                    si fósforo:
                        valor = fósforo.grupo(7).banda()
                    demás:
                        valor = ' '.unirse(regiones[6:])
                
                si nombre y valor:
                    kV[nombre]= valor
                    leñador.depurar(f"Cookie extraída:{nombre}")
            excepto(Error de valor,Error de índice)como mi:
                leñador.depurar(f"Error al analizar la línea de cookies de Netscape:{línea}, error:{mi}")
                continuar
    
    leñador.información(f"Extraído{Len(kV)}cookies del formato Netscape")
    devolver kV


definición _extraer_pares_kv_cookies(texto:str)-> Diccionario[str,str]:
    limpio = re.sub(r"(?i)^\s*cookie\s*:\s*","",texto).banda()
    regiones =[pag.banda()para pag en limpio.dividir(";")si pag.banda()]
    si Len(regiones)== 1 y "\norte" en limpio:
        regiones =[pag.banda()para pag en limpio.líneas de división()si pag.banda()]

    kV:Diccionario[str,str]={}
    para parte en regiones:
        metro = COOKIE_KV_RE.fósforo(parte)
        si metro:
            k = metro.grupo(1).banda()
            v = metro.grupo(2).banda()
            kV[k]= v

    devolver kV


definición _build_cookie_header(entrada de cookies:str)-> Opcional[str]:
    """Analiza cualquier formato de cookie y crea una cadena de encabezado de cookie."""
    
    leñador.información("Intentando analizar las cookies...")
    
    # Prueba primero con el formato JSON
    si _is_json_cookie(entrada de cookies):
        leñador.información("Formato de cookie JSON detectado")
        kV = _extraer_cookies_json(entrada de cookies)
        si kV:
            devolver "; ".unirse([F"{k}={v}" para k,v en kV.elementos()])
    
    # Prueba el formato Netscape (separado por tabulaciones o espacios)
    si _is_netscape_cookie(entrada de cookies):
        leñador.información("Formato de cookie de Netscape detectado")
        kV = _extraer_cookies_netscape(entrada de cookies)
        si kV:
            resultado = "; ".unirse([F"{k}={v}" para k,v en kV.elementos()])
            leñador.información(f"Análisis realizado correctamente{Len(kV)}cookies del formato Netscape")
            devolver resultado
    
    # Prueba el formato de encabezado de cookie o clave=valor
    si _parece_encabezado_de_cookie(entrada de cookies):
        leñador.información("Cookie detectada en formato encabezado o clave=valor")
        limpio = re.sub(r"(?i)^\s*cookie\s*:\s*","",entrada de cookies).banda()
        si "=" no en limpio:
            devolver Ninguno
        
        kV = _extraer_pares_kv_cookies(entrada de cookies)
        si kV:
            devolver "; ".unirse([F"{k}={v}" para k,v en kV.elementos()])
        
        # Devolver tal cual si ya está en formato clave=valor
        devolver limpio

    # Último recurso: intentar analizar como pares clave=valor
    leñador.información("Intentando analizar como pares clave=valor")
    kV = _extraer_pares_kv_cookies(entrada de cookies)
    si kV:
        devolver "; ".unirse([F"{k}={v}" para k,v en kV.elementos()])
    
    leñador.advertencia("No se pudieron analizar las cookies en ningún formato")
    devolver Ninguno


definición Claves de cookies de vista previa segura(encabezado de cookies:str)-> str:
    nombres =[]
    para simbólico en encabezado de cookies.dividir(";"):
        simbólico = simbólico.banda()
        si "=" en simbólico:
            k = simbólico.dividir("=",1)[0].banda()
            nombres.añadir(k)
    nombres =[norte para norte en nombres si norte]
    devolver ", ".unirse(nombres[:8])+("..." si Len(nombres)> 8 demás "")


URL de la API de NFTOKEN = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"
PARÁMETROS_DE_CONSULTA_NFTOKEN ={
    "appVersion":"15.48.1",
    "configurar":'{"gamesInTrailersEnabled":"false","isTrailersEvidenceEnabled":"false","cdsMyListSortEnabled":"true","kidsBillboardEnabled":"true","addHorizontalBoxArtToVideoSummariesEnabled":"false","skOverlayTestEnabled":"false","homeFeedTestTVMovieListsEnabled":"false","baselineOnIpadEnabled":"true","trailersVideoIdLoggingFixEnabled":"true","postPlayPreviewsEnabled":"false","bypassContextualAssetsEnabled":"false","r oarEnabled":"false","useSeason1AltLabelEnabled":"false","disableCDSSearchPaginationSectionKinds":["searchVideoCarousel"],"cdsSearchHorizontalPaginationEnabled":"true","searchPreQueryGamesEnabled":"true","kidsMyListEnabled":"true","billboardEnabled":"true","useCDSGalleryEnabled":"true","contentWarningEnabled":"true","videosInPopularGamesEnabled":"true","avifFormatEnabled":"false","sharksEnabled":"true"}',
    "tipo_de_dispositivo":"NFAPPL-02-",
    "esn":"NFAPPL-02-IPHONE8%3D1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "modismo":"teléfono",
    "Versión de iOS":"15.8.5",
    "esTableta":"FALSO",
    "lenguajes":"en-US",
    "lugar":"en-US",
    "maxDeviceWidth":"375",
    "modelo":"saget",
    "tipo de modelo":"IPHONE8-1",
    "odpAware":"verdadero",
    "camino":'["cuenta","token","predeterminado"]',
    "formato de ruta":"gráfico",
    "Densidad de píxeles":"2.0",
    "progresivo":"FALSO",
    "formato de respuesta":"json",
}

ENCABEZADOS_NFTOKEN ={
    "Agente de usuario":"Argo/15.48.1 (iPhone; iOS 15.8.5; Escala/2.00)",
    "x-netflix.request.attempt":"1",
    "x-netflix.request.client.user.guid":"A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.context.profile-guid":"A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.request.routing":'{"path":"/nq/mobile/nqios/~15.48.0/user","control_tag":"iosui_argo"}',
    "x-netflix.context.app-version":"15.48.1",
    "x-netflix.argo.translated":"verdadero",
    "x-netflix.context.form-factor":"teléfono",
    "x-netflix.context.sdk-version":"2012.4",
    "x-netflix.client.appversion":"15.48.1",
    "x-netflix.context.max-device-width":"375",
    "x-netflix.context.ab-tests":"",
    "x-netflix.tracing.cl.useractionid":"4DC655F2-9C3C-4343-8229-CA1B003C3053",
    "x-netflix.client.type":"argo",
    "x-netflix.client.ftl.esn":"NFAPPL-02-IPHONE8=1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "x-netflix.context.locales":"en-US",
    "x-netflix.context.top-level-uuid":"90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "aceptar-lenguaje":"en-US;q=1",
    "x-netflix.argo.abtests":"",
    "x-netflix.context.os-version":"15.8.5",
    "x-netflix.request.client.context":'{"appState":"foreground"}',
    "x-netflix.context.ui-flavor":"argo",
    "x-netflix.argo.nfnsm":"9",
    "x-netflix.context.pixel-density":"2.0",
    "x-netflix.request.toplevel.uuid":"90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "x-netflix.request.client.timezoneid":"Asia/Daca",
}


definición _extraer_netflix_id_del_encabezado_de_la_cookie(encabezado de cookies:str)-> Opcional[str]:
    para simbólico en encabezado de cookies.dividir(";"):
        simbólico = simbólico.banda()
        si no simbólico o "=" no en simbólico:
            continuar
        k,v = simbólico.dividir("=",1)
        si k.banda().más bajo()== "netflixid":
            devolver v.banda()
    devolver Ninguno


definición _generar_nftoken(encabezado de cookies:str,tiempo_de_espera:entero = 20)-> Tupla[booleano,str,Opcional[str]]:
    netflix_id = _extraer_netflix_id_del_encabezado_de_la_cookie(encabezado de cookies)
    si no netflix_id:
        devolver FALSO,"Cookie no válida o caducada. No se encontró NetflixId.",Ninguno

    encabezados = diccionario(ENCABEZADOS_NFTOKEN)
    encabezados["Galleta"]= f"NetflixId={netflix_id}"

    intentar:
        r = solicitudes.conseguir(
            URL de la API de NFTOKEN,
            parámetros=PARÁMETROS_DE_CONSULTA_NFTOKEN,
            encabezados=encabezados,
            se acabó el tiempo=tiempo_de_espera,
            verificar=FALSO,
        )
        r.elevar_para_estado()
        datos = r.json()

        td =((((datos.conseguir("valor")o{}).conseguir("cuenta")o{}).conseguir("simbólico")o{}).conseguir("por defecto")o{})
        nftoken = td.conseguir("simbólico")

        si no nftoken:
            devolver FALSO,"Cookie no válida o caducada. Falló la generación del token.",Ninguno

        devolver Verdadero,"La API de tokens devolvió un nftoken válido.",nftoken
    excepto Excepción como mi:
        leñador.error(f"Error al generar el token nf:{mi}")
        devolver FALSO,"Cookie no válida o caducada.",Ninguno


definición _texto_desordenado(texto:str)-> str:
    si no texto:
        devolver "Desconocido"
    devolver str(texto)
    
definición decodificar_texto(valor):
    si valor es Ninguno:
        devolver "Desconocido"

    valor = str(valor)

    intentar:
        # Decodificar \x20, \uXXXX, etc.
        valor = códecs.descodificar(valor,"unicode_escape")
    excepto Excepción:
        aprobar

    # Decodificar entidades HTML
    valor = html.escapar(valor)

    # Eliminar cualquier secuencia de escape restante
    valor = re.sub(r'\\x([0-9A-Fa-f]{2})',
                   lambda metro:bytes.fromhex(metro.grupo(1)).descodificar('latino1'),
                   valor)

    devolver valor.banda()

definición _check_netflix_cookie(encabezado de cookies:str,tiempo_de_espera:entero = 25)-> Diccionario[str,str]:
    diccionario de cookies:Diccionario[str,str]={}
    para simbólico en encabezado de cookies.dividir(";"):
        simbólico = simbólico.banda()
        si no simbólico o "=" no en simbólico:
            continuar
        k,v = simbólico.dividir("=",1)
        diccionario de cookies[k.banda()]= v.banda()

    si no diccionario de cookies.conseguir("NetflixId"):
        devolver{"OK":FALSO,"razón":"No se encontró ningún NetflixId en las cookies"}

    sesión = solicitudes.Sesión()
    sesión.galletas.actualizar(diccionario de cookies)

    encabezados ={
        "Agente de usuario": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, como Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Aceptar":"texto/html,aplicación/xhtml+xml",
        "Aceptar-Lenguaje":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate",
    }

    URL =[
        "https://www.netflix.com/TuCuenta",
        "https://www.netflix.com/account",
        "https://www.netflix.com/account/membership",
    ]

    intentar:
        resp = Ninguno
        TXT = ""
        para URL en URL:
            intentar:
                r = sesión.conseguir(URL,encabezados=encabezados,se acabó el tiempo=tiempo_de_espera,permitir redirecciones=Verdadero,verificar=FALSO)
                si r.código_de_estado == 200 y "Cuenta" en(r.texto o ""):
                    resp = r
                    TXT = r.texto o ""
                    romper
            excepto Excepción:
                continuar

        si no resp o resp.código_de_estado != 200:
            devolver{"OK":FALSO,"razón":f"HTTP{resp.código_de_estado si resp demás 'error'}"}

        si("acceso" en(resp.URL o "").más bajo())o("iniciar sesión" en(resp.URL o "").más bajo()):
            devolver{"OK":FALSO,"razón":"Redireccionado a la página de inicio de sesión"}

        definición encontrar(patrón:str)-> Opcional[str]:
            metro = re.buscar(patrón,TXT)
            devolver decodificar_texto(metro.grupo(1))si metro demás Ninguno

        nombre = encontrar(r'"accountOwnerName"\s*:\s*"([^"]+)"')o encontrar(r'"firstName"\s*:\s*"([^"]+)"')
        plan_raw = encontrar(r'localizedPlanName.{1,50}?value":"([^"]+)"')o encontrar(r'"planName"\s*:\s*"([^"]+)"')
        plan = plan_raw o Ninguno
        país =(
            encontrar(r'"countryOfSignup"\s*:\s*"([^"]+)"')
            o encontrar(r'"countryCode"\s*:\s*"([^"]+)"')
            o encontrar(r'"currentCountry"\s*:\s*"([^"]+)"')
        )
        correo electrónico =(
            encontrar(r'"emailAddress"\s*:\s*"([^"]+)"')
            o encontrar(r'"email"\s*:\s*"([^"]+)"')
            o encontrar(r'"loginId"\s*:\s*"([^"]+)"')
        )
        miembro_desde = encontrar(r'"memberSince":"([^"]+)"')
        siguiente_facturación =(
            encontrar(r'"nextBillingDate":\{[^}]*"date":"([^T"]+)"')
            o encontrar(r'"nextBilling"[^}]*"value":"([^"]+)"')
        )
        precio_del_plan =(
            encontrar(r'"planPrice":\{"fieldType":"String","value":"([^"]+)"')
            o encontrar(r'"formattedPlanPrice"\s*:\s*"([^"]+)"')
        )
        pago =(
            encontrar(r'"paymentMethod":\{"fieldType":"String","value":"([^"]+)"')
            o encontrar(r'"paymentMethodType"\s*:\s*"([^"]+)"')
        )
        tarjeta =(
            encontrar(r'"paymentCardDisplayString"\s*:\s*"([^"]+)"')
            o encontrar(r'"displayText"\s*:\s*"([^"]+)"')
        )
        teléfono =(
            encontrar(r'"phoneNumberDigits":\{[^}]*"value":"([^"]+)"')
            o encontrar(r'"phoneNumber"\s*:\s*"([^"]+)"')
        )
        versión_del_teléfono = "Sí" si re.buscar(r'"isVerified":true',TXT)demás "No" si re.buscar(r'"isVerified":false',TXT)demás Ninguno
        calidad =(
            encontrar(r'"videoQuality":\{"fieldType":"String","value":"([^"]+)"')
            o encontrar(r'"maxVideoQuality"\s*:\s*"([^"]+)"')
        )
        corrientes =(
            encontrar(r'"maxStreams":\{"fieldType":"Numeric","value":([0-9]+)')
            o encontrar(r'"maxStreams"\s*:\s*"?([0-9]+)"?')
        )
        sostener = "Sí" si re.buscar(r'"isUserOnHold":true',TXT)demás "No" si re.buscar(r'"isUserOnHold":false',TXT)demás Ninguno
        extra = "Sí" si re.buscar(r'"showExtraMemberSection":\{"fieldType":"Boolean","value":true',TXT)demás "No" si re.buscar(r'"showExtraMemberSection"',TXT)demás Ninguno
        versión del correo electrónico = "Sí" si re.buscar(r'"correo electrónico verificado"\s*:\s*verdadero',TXT)demás "No" si re.buscar(r'"correo electrónico verificado"\s*:\s*falso',TXT)demás Ninguno
        guía = encontrar(r'"userGuid":\s*"([^"]+)"')o encontrar(r'"ownerGuid":\s*"([^"]+)"')

        coincidencia de estado = re.buscar(r'"membershipStatus":\s*"([^"]+)"',TXT)
        EM = coincidencia de estado.grupo(1)si coincidencia de estado demás Ninguno

        es_premium = EM == "MIEMBRO_ACTUAL" si EM demás booleano(plan y "gratis" no en str(plan).más bajo())
        tiene_cuenta =("Cuenta" en TXT)
        si no tiene_cuenta:
            devolver{"OK":FALSO,"razón":"No se encontraron datos de la cuenta"}

        perfiles:lista =[]
        intentar:
            rol = sesión.conseguir("https://www.netflix.com/ManageProfiles",se acabó el tiempo=15,verificar=FALSO)
            si rol.código_de_estado == 200:
                perfiles = re.encontrar todo(r'"profileName"\s*:\s*"([^"]+)"',rol.texto o "")
                si no perfiles:
                    perfiles = re.encontrar todo(r'"displayName"\s*:\s*"([^"]+)"',rol.texto o "")
                si no perfiles:
                    perfiles = re.encontrar todo(r'"nombre"\s*:\s*"([^"]+)"',rol.texto o "")
        excepto Excepción:
            aprobar

        definición decodificar_nombre_de_perfil(nombre):
           intentar:
              nombre = códecs.descodificar(nombre,"unicode_escape")
           excepto Excepción:
              aprobar
           devolver html.escapar(nombre)

        perfiles_str =(
          ", ".unirse(decodificar_nombre_de_perfil(_texto_desordenado(pag))para pag en perfiles)
          si perfiles demás Ninguno
       )

        devolver{
            "OK":Verdadero,
            "de primera calidad":str(es_premium),
            "nombre":nombre o "Desconocido",
            "país":país o "Desconocido",
            "plan":plan o "Desconocido",
            "plan_price":precio_del_plan o "Desconocido",
            "miembro_desde":miembro_desde o "Desconocido",
            "siguiente_facturación":siguiente_facturación o "Desconocido",
            "método_de_pago":pago o "Desconocido",
            "tarjeta enmascarada":tarjeta o "Desconocido",
            "teléfono":teléfono o "Desconocido",
            "verificado por teléfono":versión_del_teléfono o "Desconocido",
            "calidad_de_video":calidad o "Desconocido",
            "max_streams":corrientes o "Desconocido",
            "en_retención_de_pago":sostener o "Desconocido",
            "miembro extra":extra o "Desconocido",
            "correo electrónico verificado":versión del correo electrónico o "Desconocido",
            "correo electrónico":correo electrónico o "Desconocido",
            "perfiles":perfiles_str o "Desconocido",
            "guía_de_usuario":guía o "Desconocido",
            "estado_de_membresía":EM o "Desconocido",
        }
    excepto Excepción como mi:
        leñador.error(f"Error al comprobar la cookie de Netflix:{mi}")
        devolver{"OK":FALSO,"razón":str(mi)}


asíncrono definición comenzar(actualizar:Actualizar,contexto:Tipos de contexto.TIPO_PREDETERMINADO):
    intentar:
        leñador.información(f"📱 /comenzar desde{actualizar.usuario efectivo.identificación}")
        esperar actualizar.mensaje.texto_de_respuesta(TEXTO DE INICIO,modo de análisis="Reducción")
    excepto Excepción como mi:
        leñador.error(f"Error al iniciar:{mi}")


asíncrono definición comando de ayuda(actualizar:Actualizar,contexto:Tipos de contexto.TIPO_PREDETERMINADO):
    intentar:
        leñador.información(f"❓ /ayuda de{actualizar.usuario efectivo.identificación}")
        esperar actualizar.mensaje.texto_de_respuesta(TEXTO DE AYUDA)
    excepto Excepción como mi:
        leñador.error(f"Error en la ayuda:{mi}")


asíncrono definición texto_de_la_cookie_de_manejo(actualizar:Actualizar,contexto:Tipos de contexto.TIPO_PREDETERMINADO):
    intentar:
        si no actualizar.mensaje:
            devolver

        ID de usuario = actualizar.usuario efectivo.identificación
        entrada de cookies =(actualizar.mensaje.texto o "").banda()
        leñador.información(f"📨 Mensaje de{ID de usuario}:{Len(entrada de cookies)}caracteres")
        
        si no entrada de cookies:
            esperar actualizar.mensaje.texto_de_respuesta("Por favor, pegue sus cookies.")
            devolver

        encabezado de cookies = _build_cookie_header(entrada de cookies)
        si no encabezado de cookies:
            esperar actualizar.mensaje.texto_de_respuesta(
                "❌ No se pudieron analizar las cookies.\norte\norte"
                "Pega uno de estos formatos:\norte"
                "• Línea de encabezado `Cookie:` completa\norte"
                "• Formato Netscape (archivo de cookies .txt) - **delimitado por tabulaciones y espacios**\norte"
                "• Formato de matriz JSON\norte"
                "• Pares clave=valor (NetflixId=..., SecureNetflixId=..., ...)\norte\norte"
                "Entonces, envíalo de nuevo."
            )
            devolver

        avance = Claves de cookies de vista previa segura(encabezado de cookies)
        mensaje = esperar actualizar.mensaje.texto_de_respuesta(
            f"🔎 Comprobando las cookies de Netflix...\norte"
            f"(Nombres de cookies detectados:{avance})"
        )

        bucle = asyncio.obtener_bucle_de_ejecución()
        OK,detalle,nftoken = esperar bucle.ejecutar_en_ejecutor(Ninguno,_generar_nftoken,encabezado de cookies)

        si OK y nftoken:
            cuenta = esperar bucle.ejecutar_en_ejecutor(Ninguno,_check_netflix_cookie,encabezado de cookies)

            enlace telefónico = f"https://www.netflix.com/unsupported?nftoken={nftoken}"
            enlace_de_escritorio = f"https://www.netflix.com/browse?nftoken={nftoken}"
            enlace de televisión = f"https://www.netflix.com/tv8?nftoken={nftoken}"

            teléfono_html = f'<a href="{enlace telefónico}">Abrir enlace</a>'
            escritorio_html = f'<a href="{enlace_de_escritorio}">Abrir enlace</a>'
            TV_html = f'<a href="{enlace de televisión}">Abrir enlace</a>'

            cuenta_ok = booleano(cuenta y cuenta.conseguir("OK")es Verdadero)
            línea_de_estado = f"Verificación:{detalle}\norte"

            cuenta_html = ""
            si cuenta_ok:
                cuenta_html =(
                    "<b>Detalles de la cuenta</b>:\norte"
                    f"• Nombre:{html.escapar(str(cuenta.conseguir('nombre','Desconocido')))}\norte"
                    f"• Plan:{html.escapar(str(cuenta.conseguir('plan','Desconocido')))}({html.escapar(str(cuenta.conseguir('precio_plan','Desconocido')))})\norte"
                    f"• Perfiles:{html.escapar(str(cuenta.conseguir('perfiles','Desconocido')))}\norte"
                    f"• País:{html.escapar(str(cuenta.conseguir('país','Desconocido')))}\norte"
                    f"• Correo electrónico:{html.escapar(str(cuenta.conseguir('correo electrónico','Desconocido')))}\norte"
                    f"• Miembro desde:{html.escapar(str(cuenta.conseguir('miembro_desde','Desconocido')))}\norte"
                    f"• Próxima facturación:{html.escapar(str(cuenta.conseguir('próxima_facturación','Desconocido')))}\norte"
                    f"• Pago retenido:{html.escapar(str(cuenta.conseguir('en_retención_de_pago','Desconocido')))}\norte"
                    f"• Pago:{html.escapar(str(cuenta.conseguir('método_de_pago','Desconocido')))}/{html.escapar(str(cuenta.conseguir('tarjeta enmascarada','Desconocido')))}\norte"
                    f"• Máximo de transmisiones:{html.escapar(str(cuenta.conseguir('max_streams','Desconocido')))}\norte"
                    f"• Teléfono:{html.escapar(str(cuenta.conseguir('teléfono','Desconocido')))}(verificado:{html.escapar(str(cuenta.conseguir('teléfono_verificado','Desconocido')))})\norte"
                    f"• Calidad del plan:{html.escapar(str(cuenta.conseguir('calidad_de_video','Desconocido')))}\norte"
                )

            estado_html = html.escapar(línea_de_estado)

            esperar mensaje.editar_texto(
                "✅ Se ha detectado una cookie válida.\norte\norte"
                "Enlaces de inicio de sesión:\norte"
                f"📱 Teléfono:{teléfono_html}\norte"
                f"🖥️ Escritorio:{escritorio_html}\norte"
                f"📺 TV:{TV_html}\norte"
                F"\norte{estado_html}"
                F"{cuenta_html}",
                modo de análisis="HTML",
                deshabilitar_vista_de_página_web=Verdadero,
            )
            leñador.información(f"✅ Validación de cookies exitosa para{ID de usuario}")
        demás:
            esperar mensaje.editar_texto(f"❌{detalle}")
            leñador.advertencia(f"❌ Falló la validación de cookies para{ID de usuario}:{detalle}")
    excepto Excepción como mi:
        leñador.error(f"Error en handle_cookie_text:{mi}",exc_info=Verdadero)
        intentar:
            esperar actualizar.mensaje.texto_de_respuesta(f"❌ Error al procesar la solicitud")
        excepto:
            aprobar


definición ejecutar_bot_en_hilo():
    """Ejecuta el bot en un hilo separado con el manejo de señales deshabilitado"""
    global solicitud
    
    leñador.información("=" * 60)
    leñador.información("🤖 BOT COMPROBADOR DE COOKIES DE NETFLIX")
    leñador.información("=" * 60)
    
    si no TOKEN_BOT:
        leñador.error("❌ ¡BOT_TOKEN no está configurado!")
        devolver
    
    intentar:
        # Crea un nuevo bucle de eventos para este hilo
        bucle = asyncio.nuevo_bucle_de_eventos()
        asyncio.establecer_bucle_evento(bucle)
        
        leñador.información("✅ Bucle de eventos creado")
        leñador.información("🏗️ Solicitud de construcción...")
        
        # Crear aplicación
        solicitud = Generador de aplicaciones().simbólico(TOKEN_BOT).construir()
        
        leñador.información("✅ Aplicación creada con éxito")
        leñador.información("📌 Añadiendo manejadores...")
        
        solicitud.agregar_manejador(Controlador de comandos("comenzar",comenzar))
        solicitud.agregar_manejador(Controlador de comandos("ayuda",comando de ayuda))
        solicitud.agregar_manejador(Controlador de mensajes(filtros.TEXTO & ~filtros.DOMINIO,texto_de_la_cookie_de_manejo))
        
        leñador.información("✅ Manipuladores registrados")
        leñador.información("🚀 Iniciando la encuesta...\norte")
        
        # Ejecutar el sondeo SIN manejadores de señales (no funcionan en subprocesos)
        bucle.ejecutar_hasta_completar(
            solicitud.ejecutar sondeo(
                actualizaciones permitidas=Actualizar.TODOS LOS TIPOS,
                señales de parada=()  # Deshabilitar el manejo de señales en el hilo
            )
        )
        
    excepto Excepción como mi:
        leñador.error(f"❌ Error del bot:{mi}",exc_info=Verdadero)
        solicitud = Ninguno
    finalmente:
        leñador.información("🛑 El bot se detuvo")


# Rutas de Flask
@app_flask.ruta("/",métodos=["CONSEGUIR"])
definición índice():
    estado_bot = "🟢 Corriendo" si solicitud demás "🔴 Detenido"
    devolver F"""
    <html>
        <head>
            <title>Bot para comprobar las cookies de Netflix</title>
            <style>
                cuerpo {{ font-family: Arial; margin: 40px; background-color: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .status {{ relleno: 20px; radio de borde: 5px; margen: 20px 0; }}
                .running {{ background-color: #d4edda; color: #155724; }}
                .stopped {{ background-color: #f8d7da; color: #721c24; }}
                h1 {{ color: #333; }}
                un {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <cuerpo>
            <div class="container">
                <h1>✅ Bot para comprobar las cookies de Netflix</h1>
                <div class="estado{'correr' si solicitud demás 'interrumpido'}">
                    <p><b>Estado del bot:</b>{estado_bot}</p>
                    <p><b>BOT_TOKEN:</b>{'✅ Conjunto' si TOKEN_BOT demás '❌ No establecido'}</p>
                    <p><b>BOT_link: <a href="https://t.me/Cook2linkbot">Redireccionar</a></b></p>
                    <p><b>Puerto:</b>{PUERTO}</p>
                </div>
                <hr>
                <p><a href="/health">Comprobar salud</a></p>
            </div>
        </body>
    </html>
    """,200


@app_flask.ruta("/salud",métodos=["CONSEGUIR"])
definición salud():
    estado = "saludable" si solicitud demás "malsano"
    devolver{
        "estado":estado,
        "bot_running":solicitud es no Ninguno,
        "bot_token_set":booleano(TOKEN_BOT),
        "marca de tiempo":tiempo.tiempo()
    },200 si solicitud demás 503


si __nombre__ == "__principal__":
    leñador.información(F"\norte📌 PUERTO:{PUERTO}")
    leñador.información(f"📌 BOT_TOKEN:{'✅ CONJUNTO' si TOKEN_BOT demás '❌ NO ESTABLECIDO'}\norte")
    
    si no TOKEN_BOT:
        leñador.error("❌ ¡La variable de entorno BOT_TOKEN no está configurada!")
        sistema.salida(1)
    
    # Iniciar el bot en un hilo en segundo plano
    hilo_bot = Hilo(objetivo=ejecutar_bot_en_hilo,demonio=FALSO)
    hilo_bot.comenzar()
    
    # Esperar a que el bot se inicialice
    tiempo.dormir(5)
    
    # Ejecutar Flask
    leñador.información(f"🚀 Iniciando el servidor Flask en el puerto{PUERTO}\norte")
    
    intentar:
        app_flask.correr(anfitrión="0.0.0.0",puerto=PUERTO,depurar=FALSO,usar_recargador=FALSO,enroscado=Verdadero)
    excepto Interrupción de teclado:
        leñador.información("🛑 Interrupción del teclado")
        sistema.salida(0)
