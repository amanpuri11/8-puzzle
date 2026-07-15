import streamlit as st
import heapq
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="AI 8-Puzzle Solver Pro", layout="wide")

st.sidebar.header("Configuration")
user_api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Enter key to enable AI analysis")

# --- 2. HEURISTIC LOGIC (The "Intelligence") ---
def get_manhattan_distance(state):
    """Calculates the sum of distances of tiles from their goal positions."""
    distance = 0
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for i in range(9):
        tile = state[i]
        if tile != 0:
            # Current coordinates
            r, c = divmod(i, 3)
            # Goal coordinates
            goal_idx = goal.index(tile)
            gr, gc = divmod(goal_idx, 3)
            distance += abs(r - gr) + abs(c - gc)
    return distance

# --- 3. SEARCH LOGIC ---
class PuzzleSolver:
    def __init__(self, start):
        self.start = tuple(start)
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def count_inversions(self, state):
        arr = [tile for tile in state if tile != 0]
        return sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])

    def solve(self):
        if self.count_inversions(self.start) % 2 != 0: 
            return None, 0
        
        # Priority Queue stores: (priority, current_state, path)
        # Priority = g(n) + h(n)
        h_start = get_manhattan_distance(self.start)
        queue = [(h_start, self.start, [])]
        visited = {self.start: 0}
        nodes_explored = 0
        
        while queue:
            f, current, path = heapq.heappop(queue)
            nodes_explored += 1
            
            if current == self.goal: 
                return path, nodes_explored
            
            z = current.index(0); r, c = divmod(z, 3)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    n = list(current); nid = nr*3 + nc
                    n[z], n[nid] = n[nid], n[z]; neighbor = tuple(n)
                    
                    new_g = len(path) + 1
                    # Only explore if this is a shorter path to this neighbor
                    if neighbor not in visited or new_g < visited[neighbor]:
                        visited[neighbor] = new_g
                        h = get_manhattan_distance(neighbor)
                        heapq.heappush(queue, (new_g + h, neighbor, path + [neighbor]))
                        
        return None, nodes_explored

# --- 4. UI LAYOUT ---
st.title("Professional AI 8-Puzzle Solver")
st.markdown("---")

main_col1, main_col2 = st.columns([1, 1.5])

with main_col1:
    st.subheader("Input Matrix")
    if st.button("Reset Grid", use_container_width=True):
        for i in range(9): st.session_state[f"p_{i}"] = "Empty"
        st.rerun()

    input_grid = []
    for i in range(3):
        row_cols = st.columns(3)
        for j in range(3):
            with row_cols[j]:
                options = ["Empty"] + [str(x) for x in range(1, 9)]
                val = st.selectbox(f"R{i+1} C{j+1}", options, key=f"p_{i*3+j}")
                input_grid.append(0 if val == "Empty" else int(val))
    
    solve_pressed = st.button("Solve Now", type="primary", use_container_width=True)

with main_col2:
    st.subheader("Analysis & Solution")
    
    if solve_pressed:
        if len(set(input_grid)) != 9:
            st.error("Error: Please ensure numbers 1-8 and 'Empty' are each used once.")
        else:
            solver = PuzzleSolver(input_grid)
            inv = solver.count_inversions(input_grid)
            
            if inv % 2 != 0:
                st.error(f"Unsolvable State (Inversions: {inv}).")
            else:
                with st.spinner("Calculating optimal path using A*..."):
                    solution, nodes = solver.solve()
                    
                    perf_col1, perf_col2 = st.columns(2)
                    perf_col1.metric("States Explored", nodes)
                    perf_col2.metric("Total Moves", len(solution))
                    
                    st.success(f"Optimal path found in {len(solution)} moves.")
                    
                    st.markdown("### Step-by-Step Visualization")
                    for i in range(0, len(solution), 2):
                        step_cols = st.columns(2)
                        for j in range(2):
                            idx = i + j
                            if idx < len(solution):
                                with step_cols[j]:
                                    st.info(f"Move {idx+1}")
                                    s = solution[idx]
                                    st.code(f"| {s[0] or ' '} | {s[1] or ' '} | {s[2] or ' '} |\n"
                                            f"| {s[3] or ' '} | {s[4] or ' '} | {s[5] or ' '} |\n"
                                            f"| {s[6] or ' '} | {s[7] or ' '} | {s[8] or ' '} |")

    st.markdown("---")
    st.subheader("Technical AI Analysis")
    
    if not user_api_key:
        st.info("Enter API Key in sidebar for heuristic deep-dive.")
    elif solve_pressed:
        with st.spinner("Analyzing..."):
            try:
                genai.configure(api_key=user_api_key)
                gemini = genai.GenerativeModel('gemini-2.5-flash') 
                prompt = (f"Explain how the Manhattan Distance heuristic minimized the "
                         f"states explored to {nodes} for this state: {input_grid}. "
                         f"Briefly explain why {inv} inversions makes it solvable.")
                response = gemini.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"API Error: {str(e)}")