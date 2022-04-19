from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

url = 'https://www.kabum.com.br/busca?query='

def search(modelo):
	
	chrome_options = Options()
	#Deixa o WebDriver em segundo plano
	chrome_options.add_argument('--headless')
	#Não exibe as mensagens do webDriver no terminal
	chrome_options.add_argument('--log-level=3')

	navegador = webdriver.Chrome('webScraping\chromedriver.exe',options=chrome_options)
	print('Loading ...')
	navegador.get(f'{url}{modelo}')
	
	#Pega os cards dos produtos
	produts_cards = navegador.find_elements_by_xpath('//*[@id="listing"]/article/section/div[2]/div/main/div')

	#Verifica se há resultados do produto pesquisado
	if not produts_cards:
		print('\nMensagem: Produto não consta no site')

		return None
	else:

		products_urls = []

		#Pega o url de cada card e adiciona na lista
		for card in produts_cards:

			tagA = card.find_element_by_tag_name('a')		
			product_url = tagA.get_attribute('href')

			products_urls.append(product_url)
		
		#Verifica o modelo do produto buscado nas páginas resultantes da pesquisa no site
		for url_product in products_urls:

			navegador.get(url_product)

			try:
				#Pega a tag 'p' que contém o modelo do produto na página
				modelo_site = navegador.find_element_by_xpath('//*[@id="secaoInformacoesTecnicas"]/div/div[2]/div[1]/p[3]').text
			except Exception as e:
				print(f'Error: {e}')
				print('Mensagem: Tag p não encontrada, procurando por tag span')
				modelo_site = navegador.find_element_by_xpath('//*[@id="secaoInformacoesTecnicas"]/div/div[2]/div[1]/div/div[3]/span').text

			#Verifica se o modelo inserido e modelo desejado são o mesmo
			match = re.search(modelo, modelo_site)

			if match:
				print('\nMensagem: Página do produto encontrada')

				spot_price = navegador.find_element_by_xpath('//*[@id="blocoValores"]/div[2]/div/h4').text
				installment_price = navegador.find_element_by_xpath('//*[@id="blocoValores"]/div[3]/b').text
				site = url_product

				break
		
		navegador.quit()

		try:
			return spot_price, installment_price, site
		except:
			return None

#Inserir modelo do produto	
spot_price, installment_price, site = search('CT2000MX500SSD1')

print('\nPreço à vista: ' + spot_price + 
	'\nPreço parcelado: ' + installment_price + 
	'\nSite: ' + site)