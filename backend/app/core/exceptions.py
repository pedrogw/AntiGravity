class DomainException(Exception):
    def __init__(self, detail: str = "Erro interno", status_code: int = 500):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

    def __str__(self) -> str:
        return self.detail


class EntityNotFoundException(DomainException):
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(detail=detail, status_code=404)


class InvalidCredentialsException(DomainException):
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(detail=detail, status_code=401)


class ConflictException(DomainException):
    def __init__(self, detail: str = "Conflito"):
        super().__init__(detail=detail, status_code=409)


class InvalidTransitionException(DomainException):
    def __init__(self, detail: str = "Transição inválida"):
        super().__init__(detail=detail, status_code=422)
