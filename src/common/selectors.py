LOGIN = {
    "EDP_LOGO": "a.edp-logo-inline",
    "ACCEPT_COOKIES": "button#onetrust-accept-btn-handler",
    "PARA_SUA_CASA": "a#login-atual-button",
    "ESTADO_SP": "//form[@class='login-form']//div[@class='radio-input']/label[@for='option-2']",
    "USERNAME": "input[placeholder='E-mail']",
    "PASSWORD": "input[placeholder='Senha']",
    "LOGIN_BTN": "//button[@class='edp-btn edp-btn-dark login-form ignore-unobtrusive']",
    "CAPTCHA": "textarea#g-recaptcha-response-100000",
}

INSTALACOES = {
    "HEADER": "//h2[contains(.,'Minhas instalações')]",
    "INST": "//a[@data-instalacao='{instalacao}']",
}

TELA_INSTALACAO = {
    "INST_NUMBER": "//button[@class='account-dropdown dropdown-toggle green' and contains(.,'{instalacao}')]",
    "BILLS_EXTRACTS": "//div[@class='col-md-3 text-right d-none d-sm-block align-self-center']//a[@class='edp-btn edp-btn--secondary edp-btn--outline edp-btn--bg w-100 text-left' and contains(.,'Abrir essa conta')]",
}  # type: ignore

SELECT_BILL = {
    "BILL_TAB": "//button[contains(@data-target,'#MES_FILTRO') and contains(.,'{DATA}')]",
    "OPEN_BILL": "(//a[contains(@class, 'card card-extrato') and contains(.,'Visualizar fatura')])[1]",
    "DOWNLOAD_BILL": "//div[@id='box-dados-fatura']//a/i[contains(@class,'icon-big d-block pe-7s-cloud-download')]",
    "CLOSE_MODAL": "//i[@class='icon-edp-circle-error fs-1']",
}
