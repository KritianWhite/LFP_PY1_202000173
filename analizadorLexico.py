from inspect import isframe
import webbrowser
from prettytable import PrettyTable

class Token:
    def __init__(self, lexema : str, fila : int, columna : int, tipo : str ):
        self.lexema = lexema
        self.fila = fila
        self.columna = columna 
        self.tipo = tipo
    
    #def imprimirData(self):
     #  print(self.lexema, self.fila, self.columna, self.tipo)

class Error:
    def __init__(self, descripcion : str, fila : int, columna : int):
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

    #def imprimirData(self):
     #   print(self.descripcionError, self.fila, self.columna)

class analizadorLexico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.fila  = 1
        self.columna = 1
        self.buffer = ''
        self.estado = 0
        self.i = 0
        self.abierto = False

    def listTokens(self, caracter, fila, columna, token):
        self.listaTokens.append(Token(caracter, fila, columna, token))
        self.buffer = ''

    def Errores(self, caracter, fila, columna):
        self.listaErrores.append(Error('Caracter \'' + caracter + '\' no se reconoce', fila, columna ))


    '''---------------------ESTADO 0-------------------------'''
    def S0(self, caracter):
        if caracter.isalpha() and not self.abierto:
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        elif caracter == '~':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter == '<':
            self.estado = 3 
            self.buffer += caracter
            self.columna += 1
        elif caracter == '>':
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        elif caracter == '\"':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
        elif caracter == '\'':
            self.estado = 6
            self.buffer += caracter
            self.columna += 1
        elif caracter.isalpha() and self.abierto:
            self.estado = 7
            self.buffer += caracter
            self.columna += 1
        elif caracter =='[':
            self.estado = 8
            self.buffer += caracter
            self.columna += 1
        elif caracter ==']':
            self.estado = 9
            self.buffer += caracter
            self.columna += 1
        elif caracter == ':':
            self.estado = 10 
            self.buffer += caracter
            self.columna += 1
        elif caracter == ',':
            self.estado = 11
            self.buffer += caracter 
            self.columna += 1
        elif caracter == '\n':
            self.fila += 1
            self.columna += 1
        elif caracter in ['\t', ' ']:
            self.columna += 1
        elif caracter == '$':
            pass
        else:
            self.columna += 1
            self.Errores(caracter, self.fila, self.columna)
        
    '''---------------------ESTADO 1--------------------------'''    
    def S1(self, caracter):
        if caracter.isalpha():
            self.estado = 1
            self. buffer += caracter
            self.columna += 1
        else:
            if self.buffer in ['formulario', 'valor', 'valores', 'tipo', 'fondo', 'evento']:
                self.listTokens(self.buffer, self.fila, self.columna, 'Palabra reservada ' + self.buffer)
                self.estado = 0
                self.i -= 1

    def S2(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'Aña')
        self.estado = 0
        self.i -= 1
    
    def S3(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'MenorQue')
        self.estado = 0
        self.i -= 1
    
    def S4(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'mayorQue')
        self.estado = 0
        self.i -= 1
    
    def S5(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'comillas')
        self.estado = 0
        self.i -= 1
        if self.abierto:
            self.abierto = False
        else:
            self.abierto = True
    
    def S6(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'comillaSimples')
        self.estado = 0
        self.i -= 1
        if self.abierto:
            self.abierto = False
        else:
            self.abierto = True

    def S7(self, caracter):
        if caracter.isalpha():
            self.estado = 7
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 7
            self.buffer += caracter
            self.columna += 1
        elif caracter ==  ' ':
            self.estado = 7 
            self.buffer += caracter
            self.columna += 1
        elif caracter == '-':
            self.estado = 7
            self.buffer += caracter
            self.columna += 1
        elif caracter == ':':
            self.estado = 7
            self.buffer += caracter
            self.columna += 1
        else:
            self.listTokens(self.buffer, self.fila, self.columna, 'valor')
            self.estado = 0
            self.i -= 1
    
    def S8(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'corcheteAbierta')
        self.estado = 0
        self.i -= 1
    
    def S9(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'cocheteCerrado')
        self.estado = 0
        self.i -= 1
    
    def S10(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'dosPuntos')
        self.estado = 0
        self.i -= 1
    
    def S11(self):
        self.listTokens(self.buffer, self.fila, self.columna, 'coma')
        self.estado = 0
        self.i -= 1
    
    def analizar(self, cadena):
        cadena += '$'
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.S0(cadena[self.i])
            elif self.estado == 1:
                self.S1(cadena[self.i])
            elif self.estado == 2:
                self.S2()
            elif self.estado == 3:
                self.S3()
            elif self.estado == 4:
                self.S4()
            elif self.estado == 5:
                self.S5()
            elif self.estado == 6:
                self.S6()
            elif self.estado == 7:
                self.S7(cadena[self.i])
            elif self.estado == 8:
                self.S8()
            elif self.estado == 9:
                self.S9()
            elif self.estado == 10:
                self.S10()
            elif self.estado == 11:
                self.S11()
            self.i += 1

    def imprimirTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema", "linea", "columna", "tipo"]
        for token in self.listaTokens:
            x.add_row([token.lexema, token.fila, token.columna, token.tipo])
        #print('hola')
        print(x)

    def imprimirErrores(self):
        x = PrettyTable()
        x.field_names = ["Descripcion", "Linea", "Columna"]
        for error in self.listaErrores:
            x.add_row([error.descripcion, error.linea, error.columna])
        print(x)

class clasificacion:
    def obtenerComponentes(self, tokens):
        componentes = []
        for i in range(len(tokens)):
            componente = {}
            if tokens[i].tipo == 'Palabra reservada tipo' and tokens[i+3].lexema == 'etiqueta':
                componente[tokens[i].lexema] = tokens[i + 3].lexema
                for x in range(i, len(tokens)):
                    if tokens[x].lexema == '>':
                        break 
                    if tokens[x].tipo == 'Palabra reservada valor':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                componentes.append(componente)

            if tokens[i].tipo == 'Palabra reservada tipo' and tokens[i + 3].lexema == 'texto':
                componente[tokens[i].lexema] = tokens[i + 3].lexema
                for x in range(i, len(tokens)):
                    if tokens[x].lexema == '>':
                        break
                    if tokens[x].tipo == 'Palabra reservada valor':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                    if tokens[x].tipo == 'Palabra reservada fondo':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                componentes.append(componente)

            if tokens[i].tipo == 'Palabra reservada tipo' and tokens[i + 3].lexema == 'grupo-radio':
                componente[tokens[i].lexema] = tokens[i + 3].lexema
                for x in range(i,len(tokens)):
                    if tokens[x].lexema == '>':
                        break
                    if tokens[x].tipo == 'Palabra reservada valor':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                    if tokens[x].tipo == 'Palabra reservada valores':
                        grupo_radio = []
                        for h in range(x, len(tokens)):
                            if tokens[h].lexema == ']':
                                break
                            if tokens[h].tipo == 'valor':
                                grupo_radio.append(tokens[h].lexema)
                        componente[tokens[x].lexema] = grupo_radio
                componentes.append(componente)

            if tokens[i].tipo == 'Palabra reservada tipo' and tokens[i + 3].lexema == 'grupo-option':
                componente[tokens[i].lexema] = tokens[i + 3].lexema
                for x in range(i, len(tokens)):
                    if tokens[x].lexema == '>':
                        break
                    if tokens[x].tipo == "Palabra reservada valor":
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                    if tokens[x].tipo == 'Palabra reservada valores':
                        grupo_option = []
                        for h in range(x, len(tokens)):
                            if tokens[h].lexema == ']':
                                break
                            if tokens[h].tipo == 'valor':
                                grupo_option.append(tokens[h].lexema)
                        componente[tokens[x].lexema] = grupo_option
                componentes.append(componente)
            
            if tokens[i].tipo == 'Palabra reservada tipo' and tokens[i + 3].lexema == 'boton':
                componente[tokens[i].lexema] = tokens[i + 3].lexema
                for x in range(i, len(tokens)):
                    if tokens[x].lexema == '>':
                        break
                    if tokens[x].tipo == 'Palabra reservada valor':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                    if tokens[x].tipo == 'Palabra reservada evento':
                        componente[tokens[x].lexema] = tokens[x + 3].lexema
                componentes.append(componente)
        return componentes

class Reportes:
    def reporteTokens(self, tokens):

        html = """<!doctype html>
<html lang="en">
  <head>
  	<title>Reporte de Tokens</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>

	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	
	<link rel="stylesheet" href="table-07\css\style.css">

	</head>
	<body>
	<section class="ftco-section">
		<div class="container">
			<div class="row justify-content-center">
				<div class="col-md-6 text-center mb-5">
					<h2 class="heading-section">Reporte de Tokens</h2>
				</div>
			</div>
			<div class="row">
				<div class="col-md-12">
					<div class="table-wrap">
						<table class="table table-bordered table-dark table-hover">
						  <thead>
						    <tr>
						      <th>Lexema</th>
						      <th>Línea</th>
						      <th>Columna</th>
						      <th>Tipo</th>
						    </tr>
						  </thead>
						  <tbody>
        """
        for token in tokens:
            html += """
						    <tr>
						      <th scope="row">""" + token.lexema + """</th>
						      <td>""" + str(token.fila) + """</td>
						      <td>""" + str(token.columna) + """</td>
						      <td>""" + token.tipo + """</td>
						    </tr>"""
        html += """
						  </tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</section>

	<script src="js/jquery.min.js"></script>
  <script src="js/popper.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/main.js"></script>

	</body>
</html>

	<script src="js/jquery.min.js"></script>
  <script src="js/popper.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/main.js"></script>

	</body>
</html>
        
        """
        open('Reporte_Tokens.html', 'w').write(html)
        webbrowser.open('Reporte_Tokens.html')
        print("Reporte de tokens impreso")
        

    def reporteErrores(self, errores):
        html = """<!doctype html>
<html lang="en">
  <head>
  	<title>Reporte de Tokens</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>

	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	
	<link rel="stylesheet" href="table-07\css\style.css">

	</head>
	<body>
	<section class="ftco-section">
		<div class="container">
			<div class="row justify-content-center">
				<div class="col-md-6 text-center mb-5">
					<h2 class="heading-section">Reporte de Tokens</h2>
				</div>
			</div>
			<div class="row">
				<div class="col-md-12">
					<div class="table-wrap">
						<table class="table table-bordered table-dark table-hover">
						  <thead>
						    <tr>
						      <th>Descripcion</th>
						      <th>Linea</th>
						      <th>Columna</th>
						    </tr>
						  </thead>
						  <tbody>
        """
        for error in errores:
            html += """
						    <tr>
						      <th scope="row">""" + error.descripcion + """</th>
						      <td>""" + str(error.fila) + """</td>
						      <td>""" + str(error.columna) + """</td>
						    </tr>"""
        html += """
						  </tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</section>

	<script src="js/jquery.min.js"></script>
  <script src="js/popper.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/main.js"></script>

	</body>
</html>

	<script src="js/jquery.min.js"></script>
  <script src="js/popper.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/main.js"></script>

	</body>
</html>
        
        """
        open('Reporte_Errores.html', 'w').write(html)
        webbrowser.open('Reporte_Errores.html')
        print("Reporte de errores impreso")



class Formulario:
    def __init__(self):
        self.texto = 0
        self.seleccion = 0
        self.radio = 0
        self.obtenerTexto = ''
        self.radioSelect = ''
        self.obtenerListado = ''

    def mostrariframe(self, componente):
        iframe = self.inicio()
        for cmp in componente:
            if cmp['tipo'] == 'etiqueta':
                iframe += self.textoValor(cmp)
            elif cmp['tipo'] == 'texto':
                iframe += self.inputText(cmp)
            elif cmp['tipo'] == 'grupo-radio':
                iframe += self.Grupo_Radio(cmp)
            elif cmp['tipo'] == 'grupo-option':
                iframe += self.Grupo_Option(cmp)
            elif cmp['tipo'] == 'boton':
                iframe += self.Boton(cmp)
        
        iframe += self.fin()

        open('Formulario iframe.html', 'w').write(iframe)
        webbrowser.open('Formulario iframe.html')
        print('Se mostrará el formulario iframe.')

    def Boton(self, diccionario):
        iframe = """
                    <div class="container-contact100-form-btn">
					<button class="contact100-form-btn">
						<span>""" + self.llave(diccionario) + """<i class="fa fa-long-arrow-right m-l-7" aria-hidden="true"></i>
						</span>
					</button>
				</div>
        """
        return iframe
    
    def Grupo_Option(self, diccionario):
        self.seleccion += 1
        iframe = """
                    <div class="wrap-input100 input100-select bg1">
					    <span class="label-input100">""" + self.llave(diccionario) + """</span>
					    <div>
						    <select id=\"opciones""" + str(self.seleccion) + """\" class="js-select2" name="service">
                            <option disabled selected>Elija una opcion *</option>
                            """ + self.opciones(diccionario['valores']) + """
                            </select>
						    <div class="dropDownSelect2"></div>
					    </div>
				    </div>
        """
        return iframe

    def opciones(self, listaOpciones):
        iframe = ''
        for x in listaOpciones:
            iframe +="""
                        <option>""" + x + """</option>
            """
        return iframe

    def Grupo_Radio(self, diccionario):
        self.radio += 1
        iframe = """
                <div class="wrap-contact100-form-radio">
					<span class="label-input100">""" + self.llave(diccionario) + """</span>
                    """ + self.radios(diccionario['valores']) +"""
				</div>
        """
        return iframe
    
    def radios(self, listaRadios):
        iframe = ''
        for rad in listaRadios:
            iframe += """
                        <div class="contact100-form-radio">
						    <input class="input-radio100" id=\"radio1""" + rad + """\" type="radio" name="type-product" value="digital" checked="checked">
						    <label class="label-radio100" for="radio1">""" + rad +"""</label>
					    </div>  
            """
        return iframe
    
    def inputText(self, diccionario):
        self.texto += 1
        iframe = """
                    <div class="wrap-input100 validate-input bg1" data-validate="Ingrese un nombre válido">
                    """ + str(self.textoValor(diccionario['valor'])) + """
					    <input class="input100" type="text" name="name" placeholder=\"""" + self.fondoInput(diccionario) + """\">
				    </div>
        """
        return iframe

    def llave(self, diccionario):
        for llave in diccionario:
            if llave == 'valor':
                return diccionario['valor']
        return ''

    def fondoInput(self, diccionario):
        for llave in diccionario:
            if llave == 'fondo':
                return diccionario['fondo']
        return ''

    def textoValor(self, diccionario):
        iframe = """
					    <span class="label-input100">""" + self.llave(diccionario) + """</span>
        """
        return iframe
    
    def inicio(self):
        iframe = """
                    <!DOCTYPE html>
<html lang="en">
<head>
	<title>iframe</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
	<link rel="icon" type="image/png" href="ContactFrom_v5\images\icons\\favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\\bootstrap\css\\bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\fonts\\font-awesome-4.7.0\css\\font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\fonts\iconic\css\material-design-iconic-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\\animate\\animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\css-hamburgers\hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\\animsition\css\\animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\select2\select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\daterangepicker\daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\\vendor\\noui\\nouislider.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\css\\util.css">
	<link rel="stylesheet" type="text/css" href="ContactFrom_v5\css\main.css">
<!--===============================================================================================-->
</head>
<body>


	<div class="container-contact100" id="iframe">
		<div class="wrap-contact100">
			<form class="contact100-form validate-form">
            <span class="contact100-form-title" id ="iframe">
				i-Frame
			</span>
            """

        return iframe
    
    def fin(self):
        iframe = """
                    </form>
		</div>
	</div>



<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\jquery\jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\\animsition\js\\animsition.min.js"></script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\\bootstrap\js\popper.js"></script>
	<script src="ContactFrom_v5\\vendor\\bootstrap\js\\bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\select2\select2.min.js"></script>
	<script>
		$(".js-select2").each(function(){
			$(this).select2({
				minimumResultsForSearch: 20,
				dropdownParent: $(this).next('.dropDownSelect2')
			});


			$(".js-select2").each(function(){
				$(this).on('select2:close', function (e){
					if($(this).val() == "Please chooses") {
						$('.js-show-service').slideUp();
					}
					else {
						$('.js-show-service').slideUp();
						$('.js-show-service').slideDown();
					}
				});
			});
		})
	</script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\daterangepicker\moment.min.js"></script>
	<script src="ContactFrom_v5\\vendor\daterangepicker\daterangepicker.js"></script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\countdowntime\countdowntime.js"></script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\\vendor\\noui\\nouislider.min.js"></script>
	<script>
	    var filterBar = document.getElementById('filter-bar');

	    noUiSlider.create(filterBar, {
	        start: [ 1500, 3900 ],
	        connect: true,
	        range: {
	            'min': 1500,
	            'max': 7500
	        }
	    });

	    var skipValues = [
	    document.getElementById('value-lower'),
	    document.getElementById('value-upper')
	    ];

	    filterBar.noUiSlider.on('update', function( values, handle ) {
	        skipValues[handle].innerHTML = Math.round(values[handle]);
	        $('.contact100-form-range-value input[name="from-value"]').val($('#value-lower').html());
	        $('.contact100-form-range-value input[name="to-value"]').val($('#value-upper').html());
	    });
	</script>
<!--===============================================================================================-->
	<script src="ContactFrom_v5\js\main.js"></script>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-23581568-13');
</script>

</body>
</html>
                """
        return iframe

