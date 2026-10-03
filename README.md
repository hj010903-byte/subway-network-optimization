# Subway Network Optimization

## 1. Project Overview
학교 프로젝트학기로 수행한 서울 지하철 노선망 설계 탐색 프로젝트의 공개용 정리본입니다. 팀 프로젝트의 전체 작업을 설명하며, 개인별 역할은 제공된 자료로 확정할 수 없습니다. 실제 운영 노선의 개선 효과나 최종 최적해를 입증한 프로젝트로 표현하지 않습니다.

근거: `지하철최적화_최종성과물.ipynb`(33개 셀)와 `지하철최적화_최종발표자료.pptx`(82장). 발표 파일은 본문에서 스스로 “중간 보고서”라고 표기합니다. 원본 자료는 개인정보와 재배포 권한 검토 전이므로 저장소에 포함하지 않습니다. 이하 셀 번호는 원본의 0 기반 번호입니다.

## 2. Problem Definition
목표는 전체 역의 연결과 9개 호선 구성을 고려해 **전체 노선망을 설계하는 것**입니다. 한 출발지와 목적지 사이의 최단경로를 구하는 문제만으로는 역 포함률, 여러 노선의 조합, 간선 재사용, 경로 형태를 함께 결정할 수 없습니다. 전체 역 포함은 목표이며, 모든 실험에서 달성한 결과가 아닙니다.

## 3. Data
발표 12~14장은 서울교통공사 1~8호선 역사 좌표와 국가철도공단 수도권 9호선 역위치 자료의 병합 및 환승역 중복 제거를 설명합니다. 노트북은 이미 전처리된 Excel을 읽으며 수집·병합 과정 코드는 없습니다. 필요한 데이터 파일은 제공된 작업 폴더에서 발견되지 않았습니다. 후반 실험은 OD와 역 주변 시설 점수도 사용합니다. 구조는 [data/README.md](data/README.md)에 정리했습니다.

## 4. Why Dijkstra/A* Alone Were Not Enough
발표 7~9장은 최단경로 알고리즘의 적용 범위와 노선망 설계 목표의 차이를 설명합니다. A*는 이후 후보 경로를 생성하는 하위 도구로 계속 사용합니다. MST는 전체 연결의 기준을 탐색하지만 9개 호선의 구성과 운행 가능한 경로 형태까지 결정하지 않습니다. Dijkstra는 발표에서 검토되며 제공 노트북에 독립 구현은 없습니다.

## 5. Graph Construction
셀 6은 경도·위도를 노드 위치로 설정하고 KDTree의 가까운 이웃(k=5)을 연결합니다. 가중치는 좌표의 유클리드 거리입니다. 셀 8은 완전 그래프와 Prim MST를 실험합니다. 발표 67장은 k=30, 최대 거리 2.5km를 설명하지만 해당 서울 전역 edge 파일 생성 코드는 제공 노트북에 없습니다. 위경도 좌표 차이를 km로 해석하면 안 됩니다.

## 6. Route Generation
셀 14는 사용 가능한 간선과 미방문 노드 집합을 관리하며 경로를 확장하고 남은 노드를 기존 경로에 연결합니다. 이 과정은 분기나 반복 방문을 만들 수 있습니다. 이후 시작·종점, 외곽 노드 그룹, 2호선 순환 경로를 활용하는 방식으로 탐색을 바꿉니다. 셀 24~26은 A* 변형에 used_edges를 적용하고, 셀 26은 고정 순환 경로와 8개 종점 쌍으로 후보를 만듭니다. 탐색 실패 시 경로가 누락될 수 있습니다.

## 7. Graph Refinement
셀 22는 세 점의 변 길이를 정렬한 뒤 a²+b²<c²이면 가장 긴 변을 제거합니다. 발표 62~69장은 이를 둔각 삼각형의 “빗변 제거”로 설명합니다. 정확히는 둔각의 대변인 최장변입니다. **실제 셀 22는 세 간선이 모두 존재하는지 확인하지 않고 모든 노드 삼중쌍을 검사합니다.** 따라서 연결성을 보장하지 않으며, 현실성 개선은 정성적 관찰입니다.

## 8. Optimization Strategy
셀 26은 각 후보의 좌표 거리에 0.1~1.9의 난수를 곱하고 후보 1,000개를 만든 뒤 node coverage 상위 10개를 선별합니다. 난수 seed는 원본에 없습니다. 유전 알고리즘은 발표 5·10장의 계획이며 교차, 돌연변이, 세대 반복 구현은 제공 코드에서 확인되지 않습니다. 후반부에 실제로 구현된 것은 Simulated Annealing(셀 30)과 각도 기반 노드 재삽입 개선(셀 32)입니다. 이 추가 실험을 보존하기 위해 별도 모듈을 포함했습니다.

## 9. Results
원본 저장 출력 기준으로 셀 26의 최고 coverage는 **91.32%, 미포함 25개**입니다. 셀 30의 10회 SA 출력은 모두 **100.62→100.62**입니다. 셀 32의 종합 점수는 **18.31→20.17**입니다. 서로 다른 적합도와 실험이므로 세 수치를 직접 비교할 수 없습니다. 종합 점수는 백분율이나 실제 교통 성능 지표가 아닙니다. 데이터가 없어 이번 정리 과정에서 재현하지 않았습니다. [기록과 해석 범위](results/verified_outputs.md)를 참고하세요.

## 10. My Contribution
위 알고리즘과 실험은 팀 전체 결과로 소개합니다. 제공된 코드·발표만으로 개인 작성자와 역할별 분담을 확인할 수 없어 개인 기여를 확정하지 않았습니다. 공개 전 본인이 맡은 구현, 실험, 데이터 처리 또는 발표 범위를 팀과 확인하고 근거와 함께 이 절에 추가해야 합니다.

## 11. Limitations
최종 최적해, 실제 통행시간 개선, 운영 가능성, 전체 역 coverage 달성을 입증하지 못했습니다. 위경도 유클리드 거리, 난수 가중치와 A* 휴리스틱의 불일치, 누락 노드 및 실패 경로 처리, 재삽입 시 비인접 간선 추가, 중복 점수 집계 문제가 남아 있습니다. [상세 한계](docs/limitations.md), [정리 변경점](docs/cleanup_notes.md)을 참고하세요.

## 12. Repository Structure
```text
portfolio/
├── README.md
├── notebooks/01_subway_network_optimization.ipynb
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── graph_builder.py
│   ├── route_generator.py
│   ├── graph_refinement.py
│   ├── fitness.py
│   ├── initial_population.py
│   ├── simulated_annealing.py
│   └── individual_improvement.py
├── docs/{methodology,experiment_history,limitations,cleanup_notes}.md
├── results/{README,verified_outputs}.md
│   └── {coverage_rank1,angle_improvement}.png
├── data/README.md
├── requirements.txt
└── .gitignore
```

Python 3 환경에서 저장소 루트 기준 `python -m pip install -r requirements.txt` 후 `jupyter lab`을 실행하고 notebooks 파일을 엽니다. 데이터 준비와 단계별 실행이 필요합니다. 원본 계산을 보존한 기록용 notebook이므로 Run All은 권장하지 않습니다. `src`는 루트에서 import하는 별도 함수 API입니다. `initial_population.select_initial_population()`은 coverage 기준 초기 개체 선별만 제공합니다. GA evolution loop는 구현되지 않았으며 실행 함수도 제공하지 않습니다. 공개 SA의 `score_func` 인터페이스는 `(line_paths, od_dict, node_dict, graph)`로, `fitness.calculate_combined_fitness`를 직접 전달할 수 있습니다. 이는 원본 셀 30의 적합도 함수를 자동으로 대체한다는 뜻은 아닙니다.

원본 저장 시각화 두 장과 설명은 [results/README.md](results/README.md)에 있습니다. 실제 운영 노선도가 아닌 실험 후보입니다.
