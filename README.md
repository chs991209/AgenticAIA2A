# AgenticAIA2A

Google ADK (Agent Development Kit)를 활용한 다양한 멀티 에이전트 시스템 패턴을 구현한 프로젝트입니다. 이 프로젝트는 순차 실행, 병렬 실행, 루프 기반 워크플로우, 오케스트레이션 등 다양한 에이전트 아키텍처 패턴을 실습할 수 있는 예제들을 제공합니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [사전 요구사항](#사전-요구사항)
- [설치 방법](#설치-방법)
- [프로젝트 구조](#프로젝트-구조)
- [사용 예제](#사용-예제)
- [설정](#설정)
- [기술 스택](#기술-스택)
- [워크플로우 패턴](#워크플로우-패턴)

## 🎯 프로젝트 개요

이 프로젝트는 Google의 Agent Development Kit (ADK)을 사용하여 다양한 멀티 에이전트 시스템 패턴을 구현합니다. 각 예제는 실제 사용 사례를 기반으로 하며, 에이전트 간 협업, 작업 위임, 병렬 처리, 반복 개선 등의 개념을 학습할 수 있습니다.

## ✨ 주요 기능

- **LLM 오케스트레이터 패턴**: 메인 에이전트가 다른 에이전트를 도구로 사용하여 작업을 조율
- **순차 워크플로우**: 여러 에이전트가 순차적으로 작업을 수행하는 파이프라인
- **병렬 워크플로우**: 여러 에이전트가 동시에 독립적인 작업을 수행
- **루프 워크플로우**: 피드백 루프를 통한 반복적 개선 프로세스
- **커스텀 도구 통합**: Python 함수, 코드 실행기, 검색 도구 등을 에이전트에 통합

## 🔧 사전 요구사항

- Python 3.12 이상
- Google API Key (Gemini API)
- pip 패키지 관리자

## 📦 설치 방법

1. **저장소 클론 또는 프로젝트 디렉토리로 이동**
   ```bash
   cd AgenticAIA2A
   ```

2. **가상 환경 생성 및 활성화** (권장)
   ```bash
   python -m venv agenticai-A2A
   # Windows
   agenticai-A2A\Scripts\activate
   # Linux/Mac
   source agenticai-A2A/bin/activate
   ```

3. **필요한 패키지 설치**
   ```bash
   pip install google-adk python-dotenv
   ```

4. **환경 변수 설정**
   프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가하세요:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 📁 프로젝트 구조

```
AgenticAIA2A/
├── orchestrator-agents.py      # LLM 오케스트레이터 패턴 예제
├── sequential-agents.py        # 순차 워크플로우 예제 (블로그 작성 파이프라인)
├── parellel-agents.py          # 병렬 워크플로우 예제 (동시 리서치)
├── loop-agents.py              # 루프 워크플로우 예제 (스토리 개선)
├── agent-tools.py              # 커스텀 도구 및 코드 실행기 예제
├── sample-agent/               # 기본 에이전트 예제
│   └── agent.py
├── agenticai-A2A/             # 가상 환경 디렉토리
└── README.md                   # 프로젝트 문서
```

## 🚀 사용 예제

### 1. LLM 오케스트레이터 (orchestrator-agents.py)

메인 에이전트가 리서치 에이전트와 요약 에이전트를 도구로 사용하여 작업을 조율합니다.

```bash
python orchestrator-agents.py
```

**기능:**
- 리서치 에이전트가 Google 검색을 통해 정보 수집
- 요약 에이전트가 수집된 정보를 요약
- 코디네이터 에이전트가 전체 프로세스를 관리

### 2. 순차 워크플로우 (sequential-agents.py)

블로그 작성 파이프라인: 개요 작성 → 초안 작성 → 편집

```bash
python sequential-agents.py
```

**기능:**
- OutlineAgent: 블로그 개요 생성
- WriterAgent: 개요를 기반으로 초안 작성
- EditorAgent: 초안을 편집 및 개선

### 3. 병렬 워크플로우 (parellel-agents.py)

세 개의 리서치 에이전트가 동시에 기술, 건강, 금융 분야를 조사하고 결과를 취합합니다.

```bash
python parellel-agents.py
```

**기능:**
- TechResearcher: AI/ML 트렌드 조사
- HealthResearcher: 의학적 돌파구 조사
- FinanceResearcher: 핀테크 트렌드 조사
- AggregatorAgent: 세 가지 조사 결과를 통합 요약

### 4. 루프 워크플로우 (loop-agents.py)

스토리 작성 및 반복적 개선 프로세스

```bash
python loop-agents.py
```

**기능:**
- InitialWriterAgent: 초기 스토리 초안 작성
- CriticAgent: 스토리 비평 및 피드백 제공
- RefinerAgent: 피드백을 반영하여 스토리 개선
- 최대 2회 반복 (무한 루프 방지)

### 5. 커스텀 도구 (agent-tools.py)

커스텀 Python 함수와 코드 실행기를 사용하는 에이전트 예제

```bash
python agent-tools.py
```

**기능:**
- 커스텀 함수 도구: 환율 조회, 수수료 계산
- 코드 실행기: Python 코드를 실행하여 계산 수행
- 에이전트를 도구로 사용: 계산 에이전트를 다른 에이전트의 도구로 활용

## ⚙️ 설정

### 재시도 설정

모든 예제는 HTTP 재시도 설정을 포함하고 있습니다:

```python
retry_config = types.HttpRetryOptions(
    attempts=5,           # 최대 5회 재시도
    exp_base=7,           # 지수 백오프 베이스
    initial_delay=1,      # 초기 지연 시간 (초)
    http_status_codes=[429, 500, 503, 504],  # 재시도할 HTTP 상태 코드
)
```

### 모델 설정

현재 프로젝트는 `gemini-2.5-flash-lite` 모델을 사용합니다. 필요에 따라 다른 Gemini 모델로 변경할 수 있습니다.

```python
llm = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)
```

## 🛠️ 기술 스택

- **Google ADK (Agent Development Kit)**: 멀티 에이전트 시스템 구축을 위한 프레임워크
- **Gemini API**: Google의 대규모 언어 모델
- **Python 3.12+**: 프로그래밍 언어
- **python-dotenv**: 환경 변수 관리

## 🔄 워크플로우 패턴

### 1. 오케스트레이터 패턴
```
사용자 요청
    ↓
Coordinator Agent
    ├─→ Research Agent (도구로 사용)
    └─→ Summarizer Agent (도구로 사용)
    ↓
최종 응답
```

### 2. 순차 패턴
```
사용자 요청
    ↓
Agent 1 → Agent 2 → Agent 3
    ↓
최종 결과
```

### 3. 병렬 패턴
```
사용자 요청
    ↓
    ├─→ Agent 1 (병렬)
    ├─→ Agent 2 (병렬)
    └─→ Agent 3 (병렬)
    ↓
Aggregator Agent
    ↓
최종 결과
```

### 4. 루프 패턴
```
초기 작업
    ↓
[Critic Agent → Refiner Agent] (반복)
    ↓
조건 만족 시 종료
    ↓
최종 결과
```
