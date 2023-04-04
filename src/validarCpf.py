def validar_cpf(cpf):
    # Removendo os caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificando se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Calculando o primeiro dígito verificador
    soma = sum([int(cpf[i]) * (i + 1) for i in range(9)])
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Calculando o segundo dígito verificador
    soma = sum([int(cpf[i]) * i for i in range(10)])
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verificando se os dígitos verificadores são válidos
    if cpf[-2:] == str(digito1) + str(digito2):
        return True
    else:
        return False