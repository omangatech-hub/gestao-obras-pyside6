import pandas as pd
from pathlib import Path

class ImportadorExcel:
    """Importa materiais de um arquivo Excel"""
    
    @staticmethod
    def validar_excel(caminho_arquivo):
        """Valida se o arquivo é um Excel válido"""
        try:
            df = pd.read_excel(caminho_arquivo)
            return True, df
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def importar_materiais(caminho_arquivo, material_controller):
        """
        Importa materiais do Excel para o banco de dados
        
        Espera colunas: código, descrição, unidade, estoque (opcional)
        """
        try:
            df = pd.read_excel(caminho_arquivo)
            
            # Normaliza nomes de colunas (remove espaços, converte para minúsculas)
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
            
            # Valida colunas obrigatórias
            colunas_obrigatorias = ['código', 'descrição', 'unidade']
            colunas_presentes = list(df.columns)
            
            # Tenta encontrar as colunas mesmo com variações de nome
            mapa_colunas = {
                'codigo': None,
                'descricao': None,
                'unidade': None,
                'estoque': None
            }
            
            for col in colunas_presentes:
                col_lower = col.lower().replace('ã', 'a').replace('á', 'a')
                if 'cod' in col_lower:
                    mapa_colunas['codigo'] = col
                elif 'desc' in col_lower:
                    mapa_colunas['descricao'] = col
                elif 'unid' in col_lower:
                    mapa_colunas['unidade'] = col
                elif 'esto' in col_lower:
                    mapa_colunas['estoque'] = col
            
            # Valida se encontrou as colunas obrigatórias
            if not all([mapa_colunas['codigo'], mapa_colunas['descricao'], mapa_colunas['unidade']]):
                return False, f"Colunas obrigatórias não encontradas. Esperadas: Código, Descrição, Unidade"
            
            # Importa os materiais
            materiais_importados = 0
            erros = []
            
            for idx, row in df.iterrows():
                try:
                    codigo = str(row[mapa_colunas['codigo']]).strip() if pd.notna(row[mapa_colunas['codigo']]) else ""
                    descricao = str(row[mapa_colunas['descricao']]).strip()
                    unidade = str(row[mapa_colunas['unidade']]).strip()
                    estoque = float(row[mapa_colunas['estoque']]) if mapa_colunas['estoque'] and pd.notna(row[mapa_colunas['estoque']]) else 0
                    
                    if not descricao:
                        erros.append(f"Linha {idx+2}: Descrição vazia")
                        continue
                    
                    material_controller.criar_material(codigo, descricao, unidade, estoque)
                    materiais_importados += 1
                
                except ValueError as e:
                    erros.append(f"Linha {idx+2}: Erro ao converter dados - {str(e)}")
                except Exception as e:
                    erros.append(f"Linha {idx+2}: {str(e)}")
            
            mensagem = f"✓ {materiais_importados} materiais importados com sucesso"
            if erros:
                mensagem += f"\n\n⚠ {len(erros)} linhas com erro:\n" + "\n".join(erros[:5])
                if len(erros) > 5:
                    mensagem += f"\n... e mais {len(erros) - 5} erros"
            
            return True, mensagem
        
        except Exception as e:
            return False, f"Erro ao processar arquivo: {str(e)}"
    
    @staticmethod
    def exportar_modelo_excel(caminho_arquivo):
        """Exporta um modelo de Excel com as colunas esperadas"""
        try:
            dados = {
                'Código': ['MAT001', 'MAT002'],
                'Descrição': ['Cimento 50kg', 'Areia Média'],
                'Unidade': ['saco', 'm3'],
                'Estoque': [100, 50]
            }
            df = pd.DataFrame(dados)
            df.to_excel(caminho_arquivo, index=False)
            return True, f"Modelo exportado em: {caminho_arquivo}"
        except Exception as e:
            return False, f"Erro ao exportar modelo: {str(e)}"
