# Data structure

원본 데이터는 제공 폴더에서 발견되지 않았으며 재배포 권한도 확인되지 않아 포함하지 않았습니다. 아래는 notebook read 구문과 사용 컬럼에서 확인한 구조입니다. 직접 사용 권한을 확인한 자료를 이 폴더에 두세요. data 파일은 Git에서 기본 제외합니다.

| 파일 | 코드에서 필요한 컬럼 | 근거 |
|---|---|---|
| 역 경도 위도.xlsx | 역명, 경도, 위도; 초기 출력에는 호선도 표시 | 셀 3, 6 등, Sheet1 |
| 엣지 데이터.csv | from, to, from_lon, from_lat, to_lon, to_lat, weight | 셀 16 |
| 엣지 데이터 그룹화.xlsx | from, to 등 상세 사용은 notebook 참조 | 셀 20 |
| 둔각실험.xlsx | 경도, 위도 | 셀 22, Sheet1 |
| 엣지데이터 신규.xlsx | from, to, from_lon, from_lat, to_lon, to_lat, distance | 셀 24~32 |
| 쌍가중치_정규화_OD.xlsx | 승차_역, 하차_역, 쌍_가중치_정규화 | 셀 30, 32 |
| 총점수_정규화_역주변시설.xlsx | 역명, 총점수_정규화 | 셀 30, 32 |

발표 12~14장에 따르면 좌표의 출처는 서울교통공사 1~8호선 자료와 국가철도공단 수도권 9호선 자료입니다. 정확한 다운로드 URL, 기준일, 라이선스, 중복 제거 규칙, 시설 점수 산식 및 OD 정규화 방식은 확인되지 않았습니다. from/to는 초기에는 정수 ID, 후반에는 역명과 연결되는 식별자로 사용됩니다. 실제 자료의 식별자와 역명 매핑을 확인해야 합니다. degree 기반 거리와 km 기반 거리를 혼용하지 마세요. src 전처리 함수는 정확히 같은 역명·좌표 행만 제거하며 원본 전처리를 복원한 것이 아닙니다.

공개 `src.graph_builder.load_edge_graph()`는 후반 실험의 **distance 컬럼 schema**를 기준으로 Excel을 읽습니다. 필수 컬럼은 `from`, `to`, `from_lon`, `from_lat`, `to_lon`, `to_lat`, `distance`이며, `distance`를 그래프의 `weight` 속성에 저장합니다. 초기 `엣지 데이터.csv`의 `weight` 컬럼 schema를 자동으로 변환하거나 직접 읽는 loader가 아닙니다.
