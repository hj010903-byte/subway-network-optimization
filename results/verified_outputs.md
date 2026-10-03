# Saved output evidence

출처: 원본 notebook의 저장된 outputs. 실행 번호는 모두 비어 있으며, 이번 작업에서는 데이터 부재로 재실행하지 않았습니다. 원본 파일 SHA-256: `7ea71be824b805ea4d9fba451f2934b1d0c95ba799a3a0c690603c3ef1845725`. 수치는 해당 출력의 표시 정밀도만 보존합니다.

## Cell 26: candidate coverage
현재 source의 후보 생성 횟수는 1,000입니다. 상위 10개 결과:
```text
Requirement already satisfied: openpyxl in /usr/local/lib/python3.11/dist-packages (3.1.5)
Requirement already satisfied: et-xmlfile in /usr/local/lib/python3.11/dist-packages (from openpyxl) (2.0.0)
Top 10 Node Coverage Results
1등 포함률: 91.32% | 미포함 노드 수: 25
2등 포함률: 89.93% | 미포함 노드 수: 29
3등 포함률: 89.93% | 미포함 노드 수: 29
4등 포함률: 89.93% | 미포함 노드 수: 29
5등 포함률: 89.58% | 미포함 노드 수: 30
6등 포함률: 89.58% | 미포함 노드 수: 30
7등 포함률: 89.24% | 미포함 노드 수: 31
8등 포함률: 89.24% | 미포함 노드 수: 31
9등 포함률: 88.89% | 미포함 노드 수: 32
10등 포함률: 88.89% | 미포함 노드 수: 32
```
분모는 G_base의 노드 수입니다. 91.32%와 25개 미포함에서 분모 288개가 일관된 것으로 역산되지만, 원본 역 전체 개수와 동일한지는 확인하지 못했습니다. 서울 전체 실제 역 수로 소개하지 않습니다.

## Cell 30: Simulated Annealing
```text
[Trial 1] Original: 100.62 | Improved: 100.62
[Trial 2] Original: 100.62 | Improved: 100.62
[Trial 3] Original: 100.62 | Improved: 100.62
[Trial 4] Original: 100.62 | Improved: 100.62
[Trial 5] Original: 100.62 | Improved: 100.62
[Trial 6] Original: 100.62 | Improved: 100.62
[Trial 7] Original: 100.62 | Improved: 100.62
[Trial 8] Original: 100.62 | Improved: 100.62
[Trial 9] Original: 100.62 | Improved: 100.62
[Trial 10] Original: 100.62 | Improved: 100.62
```
표시된 정밀도에서 점수 개선이 관찰되지 않습니다. 최적성을 입증하지 않습니다.

## Cell 32: angle-based improvement
```text
before score: 18.31 → after score: 20.17
```
셀 30과 적합도 구성이 달라 직접 비교할 수 없습니다. 위 결과는 종합 점수 변화이며 coverage 증가나 교통 성능 개선을 뜻하지 않습니다. 간선 유효성과 제약 유지 여부를 별도로 검토해야 합니다.
