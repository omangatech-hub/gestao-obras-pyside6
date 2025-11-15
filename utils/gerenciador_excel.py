import pandas as pd
from pathlib import Path

class GerenciadorExcel:
    """Gerencia leitura de materiais diretamente do Excel"""
    
    def __init__(self, caminho_arquivo=None):
        self.caminho_arquivo = caminho_arquivo
        self.df = None
        self.materiais = []
    
    def carregar_arquivo(self, caminho_arquivo):
        """Carrega um arquivo Excel e lê os materiais"""
        try:
            self.caminho_arquivo = caminho_arquivo
            self.df = pd.read_excel(caminho_arquivo)
            
            # Normaliza nomes de colunas - remove acentos PRIMEIRO, depois minúsculas
            colunas_originais = self.df.columns.tolist()
            self.df.columns = [col.strip().lower().replace('ã', 'a').replace('á', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o') for col in self.df.columns]
            
            # Encontra as colunas
            colunas_presentes = list(self.df.columns)
            mapa_colunas = {
                'codigo': None,
                'descricao': None,
                'unidade': None
            }
            
            for col in colunas_presentes:
                col_lower = col.lower()
                # Verifica por padrões de coluna (acentos já removidos)
                if 'cod' in col_lower:
                    mapa_colunas['codigo'] = col
                elif 'desc' in col_lower:
                    mapa_colunas['descricao'] = col
                elif 'unid' in col_lower:
                    mapa_colunas['unidade'] = col
            
            colunas_encontradas = [k for k, v in mapa_colunas.items() if v is not None]
            if len(colunas_encontradas) < 3:
                mensagem = f"Colunas encontradas: {', '.join(colunas_encontradas)}\n"
                mensagem += f"Colunas na planilha: {', '.join(colunas_originais)}\n\n"
                mensagem += "Esperadas: Código, Descrição, Unidade"
                return False, mensagem
            
            # Extrai os materiais
            self.materiais = []
            erros = []
            
            for idx, row in self.df.iterrows():
                try:
                    codigo = str(row[mapa_colunas['codigo']]).strip() if pd.notna(row[mapa_colunas['codigo']]) else ""
                    descricao = str(row[mapa_colunas['descricao']]).strip()
                    unidade = str(row[mapa_colunas['unidade']]).strip()
                    
                    if not descricao:
                        erros.append(f"Linha {idx+2}: Descrição vazia")
                        continue
                    
                    self.materiais.append({
                        'id': idx + 1,
                        'codigo': codigo,
                        'descricao': descricao,
                        'unidade': unidade
                    })
                except Exception as e:
                    erros.append(f"Linha {idx+2}: {str(e)}")
            
            mensagem = f"✓ {len(self.materiais)} materiais carregados do Excel"
            if erros:
                mensagem += f"\n⚠ {len(erros)} linhas ignoradas"
            
            return True, mensagem
        
        except Exception as e:
            return False, f"Erro ao carregar arquivo: {str(e)}"
    
    def obter_materiais(self):
        """Retorna a lista de materiais carregados"""
        return self.materiais
    
    def obter_material_por_indice(self, indice):
        """Obtém um material específico pelo índice"""
        if 0 <= indice < len(self.materiais):
            return self.materiais[indice]
        return None
    
    def buscar_material(self, termo):
        """Busca materiais por código ou descrição"""
        termo_lower = termo.lower()
        resultados = [m for m in self.materiais 
                     if termo_lower in m['codigo'].lower() or 
                        termo_lower in m['descricao'].lower()]
        return resultados
    
    @staticmethod
    def criar_modelo_excel(caminho_arquivo):
        """Cria um arquivo modelo Excel"""
        try:
            dados = {
                'Código': ['MAT001', 'MAT002', 'MAT003'],
                'Descrição': ['Cimento 50kg', 'Areia Média', 'Brita n°1'],
                'Unidade': ['saco', 'm3', 'm3']
            }
            df = pd.DataFrame(dados)
            df.to_excel(caminho_arquivo, index=False)
            return True, f"Modelo criado em: {caminho_arquivo}"
        except Exception as e:
            return False, f"Erro ao criar modelo: {str(e)}"
