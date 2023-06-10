import pandas as pd

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers
    
    # 레벤슈타인 거리 계산하기
    def levenshtein_distance(self, input, data_set):
        # input = 입력 문장, data_set = questions / 질문 목록 리스트
        input_len = len(input) # input 길이
        dataSet_len = len(data_set) # dataSet_len 질문 목록 갯수
        cal_result = [] # 거리 계산 결과를 저장할 리스트
        
        # 2차원 표 준비하기
        for i in range(dataSet_len): # 입력문장과 전체 질문 목록 거리 구하기
            data = data_set[i] # 한개의 질문 데이터
            data_len = len(data_set[i]) # 데이터 길이
            matrix = [[] for j in range(input_len+1)] # 입력문장의 행 생성
            for j in range(input_len+1):
                matrix[j] = [0 for k in range(data_len+1)] # 입력문장과 j번째 질문의 거리를 계산하기 위한 열 생성 및 초기화
            for j in range(input_len+1):
                matrix[j][0] = j
            for k in range(data_len+1):
                matrix[0][k] = k
                
            # 표 채우기    
            for j in range(1, input_len+1):
                input_c = input[j-1]
                for k in range(1, data_len+1):
                    data_c = data[k-1] 
                    cost = 0 if (input_c == data_c) else 1 
                    matrix[j][k] = min([
                        matrix[j-1][k] + 1,     # 문자 제거: 위쪽에서 +1
                        matrix[j][k-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                        matrix[j-1][k-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                    ])
            cal_result.append(matrix[input_len][data_len]) # 결과 값 리스트에 추가하기
        return cal_result

    def find_best_answer(self, input_sentence):
        cal_distance = self.levenshtein_distance(input_sentence, self.questions) # 레벤슈타인 거리 구하기
        min_distance = cal_distance.index(min(cal_distance)) # 레벤슈타인 거리 값 중 가장 값은 값의 인덱스 구하기
        return self.answers[min_distance]

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)