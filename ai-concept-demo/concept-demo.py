import yaml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="data/malgun.ttf").get_name()
rc('font', family=font_name)

def read_subjects(filename):
    # 파일 읽기 시 예외 처리 추가
    try:
        with open(filename, 'rt', encoding='UTF8') as file:
            data = yaml.safe_load(file)
        return data.get('과목', [])
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return []
    except yaml.YAMLError:
        print("YAML 파일을 파싱하는 중 오류가 발생했습니다.")
        return []

# 학년과 학기가 같은 강좌에 대한 좌표 조정 함수
def adjust_coordinates(subjects):
    adjusted_pos = {}
    for subject in subjects:
        grade = subject['학년']
        semester = subject['학기']
        pos_key = (grade, semester)
        if pos_key in adjusted_pos:
            adjusted_pos[pos_key].append(0)
        else:
            adjusted_pos[pos_key] = [0]
    # 겹치는 노드중 하나만 이동하도록 조정 하는 함수
    for pos_key, positions in adjusted_pos.items():
        num_positions = len(positions)
        if num_positions > 1:
            spacing = 0.4
            for i in range(num_positions):
                adjusted_pos[pos_key][i] = (i - (num_positions - 1) / 2) * spacing
    return adjusted_pos

def draw_course_structure(subjects):
    G = nx.DiGraph()
    adjusted_pos = adjust_coordinates(subjects)
    for subject in subjects:
        grade = subject['학년']
        semester = subject['학기']
        #x,y 좌표 조정
        x = grade + adjusted_pos[(grade, semester)].pop(0)  
        y = semester
        G.add_node(subject['과목명'], pos=(x, y))
        if '선수과목' in subject:
            for prereq in subject['선수과목']:
                G.add_edge(prereq, subject['과목명'])

    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue",  font_family=font_name, font_size=10, font_weight="bold")
    for edge in G.edges():
        nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->', arrowsize=10)
    plt.title("과목 이수 체계도")
    plt.xticks(range(1, 5))  # 학년
    plt.yticks(range(1, 3))  # 학기
    plt.grid(True)  # 그리드 표시
    plt.show()

if __name__ == "__main__":
    filename = "input.yaml"
    subjects = read_subjects(filename)
    draw_course_structure(subjects)
