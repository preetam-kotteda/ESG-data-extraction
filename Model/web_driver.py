from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(r"https://browser.neo4j.io/?connectURL=neo4j%2Bs%3A%2F%2Fneo4j%406a12d69e.databases.neo4j.io%2F")