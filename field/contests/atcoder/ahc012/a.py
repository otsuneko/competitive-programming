def calc_score():

    pieces = []

    for i in range(len(pos_y)):
        for j in range(len(pos_x)):
            if i == 0 and j == 0:
                
	# for px, py, qx, qy in lines:
	# 	new_pieces = []
	# 	for piece in pieces:
	# 		left = []
	# 		right = []
	# 		for j in piece:
	# 			x, y = input.xy[j];
	# 			let side = (qx - px) as i64 * (y - py) as i64 - (qy - py) as i64 * (x - px) as i64;
	# 			if side > 0 {
	# 				left.push(j);
	# 			} else if side < 0 {
	# 				right.push(j);
	# 			}
	# 		}
	# 		if left.len() > 0 {
	# 			new_pieces.push(left);
	# 		}
	# 		if right.len() > 0 {
	# 			new_pieces.push(right);
	# 		}
	# 	}
	# 	pieces = new_pieces;
	# }
	# let mut b = vec![0; 10];
	# for piece in &pieces {
	# 	if piece.len() <= 10 {
	# 		b[piece.len() - 1] += 1;
	# 	}
	# }
	# let mut num = 0;
	# let mut den = 0;
	for d in 0..10 {
		num += input.a[d].min(b[d]);
		den += input.a[d];
	}
	let score = (1e6 * num as f64 / den as f64).round() as i64;
	(score, String::new(), (b, pieces))

N,K = map(int,input().split()) # K = 100
A = list(map(int,input().split()))
pos = [list(map(int,input().split())) for _ in range(N)]

lines = set()

grid = [500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000]
pos_x = set()
pos_y = set()

for pos in grid:
    lines.add((1,pos,0,pos))
    lines.add((1,-pos,0,-pos))
    lines.add((pos,1,pos,0))
    lines.add((-pos,1,-pos,0))
    pos_x.add(pos)
    pos_y.add(pos)

if N > 2000:
    grid_add = [2500]
    for pos in grid_add:
        lines.add((1,pos,0,pos))
        lines.add((1,-pos,0,-pos))
        lines.add((pos,1,pos,0))
        lines.add((-pos,1,-pos,0))
        pos_x.add(pos)
        pos_y.add(pos)

if 2500 <= N:
    grid_add = [3500]
    for pos in grid_add:
        lines.add((pos,1,pos,0))
        lines.add((-pos,1,-pos,0))
        pos_x.add(pos)

if 3000 <= N:
    grid_add = [4500]
    for pos in grid_add:
        lines.add((pos,1,pos,0))
        lines.add((-pos,1,-pos,0))
        pos_x.add(pos)

if 3500 <= N:
    grid_add = [9500]
    for pos in grid_add:
        lines.add((pos,1,pos,0))
        lines.add((-pos,1,-pos,0))
        pos_x.add(pos)

if N >= 4000 and A[0] >= 75:
    grid_add = [250]
    for pos in grid_add:
        lines.add((1,pos,0,pos))
        lines.add((1,-pos,0,-pos))
        lines.add((pos,1,pos,0))
        lines.add((-pos,1,-pos,0)) 
        pos_x.add(pos)
        pos_y.add(pos)

pos_x = sorted(list(pos_x))
pos_y = sorted(list(pos_y))

print(len(lines))
for line in lines:
    print(*line)