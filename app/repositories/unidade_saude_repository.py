from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unidade_saude import Unidade_Saude
from app.models.medico import Medico
from app.models.falta_medicamento_unidade_saude import Falta_Medicamento_Unidade_Saude
from app.models.medicamento import Medicamento
from app.models.unidade_saude_medico import Unidade_Saude_Medico

from app.schemas.medico_schema import Medico_Response
from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Login, UnidadeSaude_Response, UnidadeSaude_Detailed_Response

def db_criar_unidade_saude(
    db: Session,
    unidade_saude_create: UnidadeSaude_Create,
    senha_hasheada: str
) -> UnidadeSaude_Create | None:
      
    existente = db.scalar(
        select(Unidade_Saude).where(
            Unidade_Saude.nome_login == unidade_saude_create.nome_login
        )
    )

    if existente:
        return None

    unidade_saude: Unidade_Saude = Unidade_Saude(
        nome_login=unidade_saude_create.nome_login,
        nome_exibicao=unidade_saude_create.nome_exibicao,
        senha=senha_hasheada,
        localizacao_exibicao=unidade_saude_create.localizacao_exibicao,
        localizacao_link_mapa=unidade_saude_create.localizacao_link_mapa,
        aberto=False,
        horario_abertura=unidade_saude_create.horario_abertura,
        horario_fechamento=unidade_saude_create.horario_fechamento,
        pessoas_fila_atendimento=0,
        pessoas_atendidas=0
    )

    db.add(unidade_saude)
    db.commit()
    db.refresh(unidade_saude)

    return unidade_saude

def db_buscar_unidade_saude_nome_login(
    db: Session,
    unidade_saude_login: UnidadeSaude_Login
) -> Unidade_Saude | None:
    
    resultado_busca = db.execute(
        select(Unidade_Saude)
            .where(Unidade_Saude.nome_login == unidade_saude_login.nome_login)
    )
    return resultado_busca.scalar_one_or_none()

def db_listar_unidades_saude(db: Session) -> list[UnidadeSaude_Response]:
    result = db.execute(
        select(
            Unidade_Saude.id,
            Unidade_Saude.nome_exibicao,
            Unidade_Saude.localizacao_exibicao,
            Unidade_Saude.localizacao_link_mapa,
            Unidade_Saude.aberto,
            Unidade_Saude.horario_abertura,
            Unidade_Saude.horario_fechamento,
            Unidade_Saude.pessoas_fila_atendimento,
            Unidade_Saude.pessoas_atendidas
        )
    ).all()

    unidade_saude_response: list[UnidadeSaude_Response] = []

    for unidade in result:
        unidade_saude_response.append(
            UnidadeSaude_Response(
                id=unidade.id,
                nome_exibicao=unidade.nome_exibicao,
                localizacao_exibicao=unidade.localizacao_exibicao,
                localizacao_link_mapa=unidade.localizacao_link_mapa,
                aberto=unidade.aberto,
                horario_abertura=unidade.horario_abertura,
                horario_fechamento=unidade.horario_fechamento,
                pessoas_fila_atendimento=unidade.pessoas_fila_atendimento,
                pessoas_atendidas=unidade.pessoas_atendidas
            )
        )

    return unidade_saude_response

def db_buscar_unidade_saude_by_id(db: Session, unidade_saude_id: int) -> UnidadeSaude_Detailed_Response | None:
    result = db.execute(
        select(
            Unidade_Saude.id,
            Unidade_Saude.nome_exibicao,
            Unidade_Saude.localizacao_exibicao,
            Unidade_Saude.localizacao_link_mapa,
            Unidade_Saude.aberto,
            Unidade_Saude.horario_abertura,
            Unidade_Saude.horario_fechamento,
            Unidade_Saude.pessoas_fila_atendimento,
            Unidade_Saude.pessoas_atendidas
        )
        .where(
            Unidade_Saude.id == unidade_saude_id
        )
    )

    unidade = result.one_or_none()
    
    if unidade is None:
        return None
    
    medicos_resultado = db.execute(
        select(
            Medico.id,
            Medico.nome,
            Medico.especializacao,
            Unidade_Saude_Medico.status_medico_unidade_saude
        )
        .join(
            Unidade_Saude_Medico,
            Medico.id == Unidade_Saude_Medico.id_medico
        )
        .where(
            Unidade_Saude_Medico.id_unidade_saude == unidade_saude_id
        )
    ).all()

    medicos = [
        Medico_Response(
            id=medico.id,
            nome=medico.nome,
            especializacao=medico.especializacao,
            atendendo=medico.status_medico_unidade_saude
        )
        for medico in medicos_resultado
    ]
    
    medicamentos = db.execute(
        select(Medicamento)
        .join(
            Falta_Medicamento_Unidade_Saude,
            Medicamento.id == Falta_Medicamento_Unidade_Saude.id_medicamento
        )
        .where(
            Falta_Medicamento_Unidade_Saude.id_unidade_saude == unidade_saude_id
        )
    ).scalars().all()
    
    return UnidadeSaude_Detailed_Response(
        id=unidade.id,
        nome_exibicao=unidade.nome_exibicao,
        localizacao_exibicao=unidade.localizacao_exibicao,
        localizacao_link_mapa=unidade.localizacao_link_mapa,
        aberto=unidade.aberto,
        horario_abertura=unidade.horario_abertura,
        horario_fechamento=unidade.horario_fechamento,
        pessoas_fila_atendimento=unidade.pessoas_fila_atendimento,
        pessoas_atendidas=unidade.pessoas_atendidas,
        medicos=medicos,
        medicamentos=medicamentos
    )