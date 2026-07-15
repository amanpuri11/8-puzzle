import cv2
import numpy as np
import heapq
import sys

# --- UNIT 1: AI PROBLEM SOLVING (A* Algorithm) ---
class PuzzleSolver:
    def __init__(self, start_state):
        self.start = tuple(start_state)
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def get_manhattan(self, state):
        dist = 0
        for i, tile in enumerate(state):
            if tile != 0:
                r, c = divmod(i, 3)
                tr, tc = divmod(tile - 1, 3)
                dist += abs(r - tr) + abs(c - tc)
        return dist

    def solve(self):
        queue = [(self.get_manhattan(self.start), self.start, [])]
        visited = {self.start: 0}
        
        while queue:
            _, current, path = heapq.heappop(queue)
            if current == self.goal: return path
            
            zero_idx = current.index(0)
            r, c = divmod(zero_idx, 3)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    n_list = list(current)
                    nid = nr*3 + nc
                    n_list[zero_idx], n_list[nid] = n_list[nid], n_list[zero_idx]
                    neighbor = tuple(n_list)
                    if neighbor not in visited:
                        visited[neighbor] = len(path) + 1
                        heapq.heappush(queue, (len(path) + 1 + self.get_manhattan(neighbor), neighbor, path + [neighbor]))
        return None

# --- UNIT 3: IMAGE PROCESSING ---
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Adaptive Thresholding handles variable lighting (Unit 3)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return thresh

def main():
    cap = cv2.VideoCapture(0)
    print("System Active.")
    print("Press 'S' to solve.")
    print("Press 'ESC' to kill the program.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        processed = process_frame(frame)
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 15000:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                if len(approx) == 4:
                    # Unit 4: Feature Tracking (Drawing the bounding box)
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                    cv2.putText(frame, "PUZZLE DETECTED", (approx[0][0][0], approx[0][0][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("AI Solver (ESC to Quit)", frame)

        # --- THE KILL SWITCH LOGIC ---
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27: # 27 is the ASCII code for the Escape Key
            print("Escape key pressed. Killing program...")
            break
            
        elif key == ord('s'):
            print("Solving current state...")
            # Example scrambled state
            test_state = (1, 2, 3, 4, 0, 6, 7, 5, 8)
            solver = PuzzleSolver(test_state)
            solution = solver.solve()
            if solution:
                print(f"Solved in {len(solution)} steps!")
                for step in solution: print(step)

    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

if __name__ == "__main__":
    main()