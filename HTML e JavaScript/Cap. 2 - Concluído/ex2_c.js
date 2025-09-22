// preciso acessar os dados contidos no form
const frm = document.querySelector("form") // acessando os dados do form
const resp = document.querySelector("h3") // acessando a header onde serão alocados os resultados
// preciso trabalhar com os dados do form e jogá-los para a header
frm.addEventListener("submit", (e)=>{
    const preço = frm.inPreço.value
    const produto = frm.inProduto.value
    // promoção = 3 com desconto, cada um passa a ter 50%
    const desconto = (preço*0.5)+(2*preço)
    const terceiroProduto = preço*0.5
    resp.innerText = `${produto} - Promoção: Leve 3 por ${desconto}\n O 3º produto custa apenas R$ ${terceiroProduto} `
    e.preventDefault()
})