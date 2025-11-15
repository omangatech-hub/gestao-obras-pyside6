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
        
        Espera colunas: código, descrição, unidade
        """
        try:
            df = pd.read_excel(caminho_arquivo)
            
            # Normaliza nomes de colunas (remove espaços, converte para minúsculas)
            colunas_originais = df.columns.tolist()
            df.columns = [col.strip().lower() for col in df.columns]
            
            # Tenta encontrar as colunas mesmo com variações de nome
            mapa_colunas = {
                'codigo': None,
                'descricao': None,
                'unidade': None
            }
            
            colunas_presentes = list(df.columns)
            
            # Debug
            import sys
            print(f"DEBUG - Colunas presentes: {colunas_presentes}", file=sys.stderr)
            
            for col in colunas_presentes:
                col_lower = col.lower().replace('ã', 'a').replace('á', 'a').replace('ç', 'c').replace('é', 'e')
                print(f"DEBUG - Testando coluna: '{col}' -> '{col_lower}'", file=sys.stderr)
                
                # Verifica por padrões de coluna
                if 'cod' in col_lower:
                    print(f"DEBUG - Encontrado CÓDIGO: {col}", file=sys.stderr)
                    mapa_colunas['codigo'] = col
                elif 'desc' in col_lower:
                    print(f"DEBUG - Encontrado DESCRIÇÃO: {col}", file=sys.stderr)
                    mapa_colunas['descricao'] = col
                elif 'unid' in col_lower:
                    print(f"DEBUG - Encontrado UNIDADE: {col}", file=sys.stderr)
                    mapa_colunas['unidade'] = col
            
            print(f"DEBUG - Mapa final: {mapa_colunas}", file=sys.stderr)
            
            # Valida se encontrou as colunas obrigatórias
            colunas_encontradas = [k for k, v in mapa_colunas.items() if v is not None]
            if len(colunas_encontradas) < 3:
                mensagem = f"Colunas encontradas: {', '.join(colunas_encontradas)}\n"
                mensagem += f"Colunas na planilha: {', '.join(colunas_originais)}\n\n"
                mensagem += "Esperadas: Código, Descrição, Unidade"
                return False, mensagem
            
            # Importa os materiais
            materiais_importados = 0
            erros = []
            
            for idx, row in df.iterrows():
                try:
                    codigo = str(row[mapa_colunas['codigo']]).strip() if pd.notna(row[mapa_colunas['codigo']]) else ""
                    descricao = str(row[mapa_colunas['descricao']]).strip()
                    unidade = str(row[mapa_colunas['unidade']]).strip()
                    
                    if not descricao:
                        erros.append(f"Linha {idx+2}: Descrição vazia")
                        continue
                    
                    material_controller.criar_material(codigo, descricao, unidade)
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
                'Unidade': ['saco', 'm3']
            }
            df = pd.DataFrame(dados)
            df.to_excel(caminho_arquivo, index=False)
            return True, f"Modelo exportado em: {caminho_arquivo}"
        except Exception as e:
            return False, f"Erro ao exportar modelo: {str(e)}"

