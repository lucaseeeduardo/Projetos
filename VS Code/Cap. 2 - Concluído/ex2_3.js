// 1 - preciso pegar as informações do form e transformar em variáveis
 const frm = document.querySelector("form")
 const saídaModelo = document.querySelector("h3")
 const saídaPreço = document.querySelector("h4")

// 2 - preciso jogar na header 3 e 4 com referênciação tipo struct

frm.addEventListener("submit", (e)=>{
    modelo = frm.inModelo.value
    preço = frm.inPreço.value
    entrada = preço*0.5
    parcelas = (preço*0.5)/12
    saídaModelo.innerText = modelo
    saídaPreço.innerText = `Valor total: R$ ${preço}\nEntrada: R$ ${entrada} + 12x R$ ${parcelas.toFixed(2)}`
    e.preventDefault()
})