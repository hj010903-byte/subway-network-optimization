# Cleanup notes

원본 파일을 변경하지 않고 portfolio에 새 파일만 작성했습니다. 셀 번호는 원본 notebook의 0 기반 인덱스입니다.

| 항목 | 공개용 처리 | 원본과 차이 |
|---|---|---|
| notebook | 33개 원본 셀의 본문·계산 유지, 안내·셀 출처 추가 | 설치 명령 제거, 데이터 경로 상대화, 출력·실행 번호·Colab metadata 제거 |
| 데이터 | 파일 제외, 구조 문서 작성 | 입력 자료는 폴더에서 발견되지 않음 |
| preprocessing | 검증·정확 행 중복 제거 어댑터 추가 | 발표의 병합·환승역 통합 코드 복원이 아님 |
| graph_builder | 셀 6 KDTree 및 셀 8 Prim 함수 분리 | 작은 입력과 k 검증 추가, edge loader는 셀 26 구조 활용 |
| route_generator | 셀 26 heuristic/random_a_star 함수 추출 | 가중치 랜덤화와 종점 처리 wrapper 추가, 원본 heuristic 보존 |
| graph_refinement | 셀 22 판정 및 제거 루프 함수화 | 그래프 copy에 적용. 모든 삼중쌍 판정 규칙 보존 |
| fitness | 셀 26 coverage와 셀 32 적합도 함수 추출 | G_base 전역 의존을 graph 인자로 치환, 수식 보존 |
| initial_population | coverage 기준 초기 선별 API | genetic_algorithm.py에서 이름 변경, select_initial_population 유지, 미구현 GA 실행 함수 제거. GA evolution loop 미구현은 문서에 명시 |
| simulated_annealing | 셀 30 함수 추출 | 초기 및 이웃 score_func 호출에 graph 인자 추가. 공개 calculate_combined_fitness 인터페이스와 호환. 이웃 생성·수용 확률·냉각·반복 로직 변경 없음 |
| individual_improvement | 셀 32 두 개선 함수 추출 | fitness에 graph 인자 전달. 원본 graph 변경 및 제약 검증 한계 보존 |
| 결과 | 텍스트 수치와 셀 26·32 PNG 두 장 추출 | 그림은 원본 그대로 유지, Folium HTML·실행 로그·개인 metadata 제외 |
| 의존성 | imports로 requirements 작성 | 버전 고정하지 않음, 원본 환경 lock으로 간주 금지 |

공개용 module API와 기록용 notebook은 서로 다른 사용 방식입니다. notebook은 src 호출 방식으로 전면 재작성하지 않아 원본 실험 흐름과 계산을 검토할 수 있습니다. notebook에는 서로 독립된 여러 실험과 큰 반복 수가 그대로 남아 있습니다. 모듈화를 위해 분리한 함수들은 완성된 end-to-end 최적화 서비스가 아닙니다. 원본 알고리즘의 결함을 묵시적으로 고쳐 원래 프로젝트 성과로 만들지 않았습니다.

첨부 자료 안의 연구 계획이나 목표는 분석 근거로만 취급했습니다. 실행 지시는 사용자의 요청에서만 가져왔습니다. 개인정보를 포함할 수 있는 원본 발표·신청서·수료증·대본은 복사하지 않았습니다.

검증: 원본 폴더의 모든 최상위 파일 SHA-256이 생성 전후 동일함을 확인했습니다. 공개용 Python 파일과 notebook 코드 셀의 AST 구문 검사를 통과했습니다. 결과 PNG 두 장을 직접 확인했습니다. 데이터 파일이 없고 현재 검증 환경에 networkx/scipy가 없어 전체 실험 및 모듈 실행은 검증하지 않았습니다. 구문 검사 성공은 알고리즘 타당성 또는 실험 재현 성공을 의미하지 않습니다.

최종 검사에서 원본 코드 셀 19개의 본문이 설치 명령 제거·경로 상대화 외에는 동일함을 비교했습니다. JSON을 디코딩한 notebook 본문과 공개 텍스트의 절대경로·알려진 개인정보 패턴 검사를 통과했습니다. 생성·검증용 임시 스크립트는 제거했습니다.

공개 전 마지막 수정은 portfolio의 module API와 문서에만 적용했습니다. data/README.md에 load_edge_graph의 후반 distance schema를 명시하고 README의 구조·사용 안내를 갱신했습니다. 기록용 notebook의 원본 실험 함수 및 평가식은 이번 수정에서 변경하지 않았습니다. SA에 공개 종합 적합도를 전달할 수 있도록 호출 인터페이스만 맞췄으며, 두 원본 실험의 점수 정의를 동일하게 바꾸지는 않았습니다.

마지막 수정 검증: 작은 그래프 fixture로 공개 calculate_combined_fitness를 SA에 직접 전달하여 호출 성공을 확인했습니다. 별도 callback으로 초기 평가 및 이웃 평가 모두 같은 graph를 전달하는지 검사했고, 초기 개체 coverage 선별과 Python 구문 검사도 통과했습니다. 원본 notebook의 기록된 SHA-256과 현재 해시가 동일했습니다. 이 인터페이스 검증은 실제 데이터로 전체 실험을 재현한 것이 아니며 새로운 프로젝트 성과로 포함하지 않습니다.
