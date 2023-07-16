// preciso acessar o form e seu conteúdo
const frm = document.querySelector("form") // acessando os dados que estão dentro do form
const resp = document.querySelector("h3") // acessando a header onde será incluído conteúdo

// preciso referenciar os dados do form e fazer com que eles sejam alocados também na header
frm.addEventListener("submit", (e)=>{
    const preço = frm.inPreço.value // preço
    const tempo = Math.ceil(frm.inTempo.value/15) // tempo total/15 sempre vai dar um decimal, pois o que vale é o tempo inteiro de 15 min, se fizer preço/15min vai dar errado
    const contaPagar = Math.ceil(preço*tempo) // preço/tempo * tempo = preço R$ 
    resp.innerText = `A conta a pagar foi de: R$ ${contaPagar.toFixed(2)}`
    e.preventDefault()
})
