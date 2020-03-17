package model;

import control.EstimatorInterface;
import java.util.ArrayList;
import java.util.Random;

import static java.lang.Math.abs;

public class Localizer implements EstimatorInterface {

	private int rows, cols, head, currentPosX, currentPosY, currentHead, dim;
	private double  L, L_s, L_s2, manhattan, clicks;
	Random rand = new Random();
	private double[][] f, TT;
	private static final int SOUTH = 2;
	private static final int NORTH = 0;
	private static final int EAST = 1;
	private static final int WEST = 3;

	public Localizer(int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
		this.dim = this.rows*this.cols*this.head;
		f = new double[dim][1];
		TT = generateTT();
		L = 0.1;
		L_s = 0.05;
		L_s2 = 0.025;
		manhattan = clicks = 0;
		this.currentPosX = 0;
		this.currentPosY = 0;
		this.currentHead = 0;

		for(int i = 0; i < dim; i++) {
			f[i][0] = 1/(double)dim;
		}
	}

	public int getNumRows() {
		return rows;
	}
	
	public int getNumCols() {
		return cols;
	}
	
	public int getNumHead() {
		return head;
	}

	public double getTProb( int x, int y, int h, int nX, int nY, int nH) {
		double dX = getDiff(x, nX);
		double dY = getDiff(y, nY);

		if ((dX + dY > 1) || (dX == 0 && dY == 0)) { // step
			return 0;
		}

		switch (nH) {

			case 0:
				if (nX != x - 1)
					return 0;
				break;
			case 1:
				if (nY != y + 1)
					return 0;
				break;
			case 2:
				if (nX != x + 1)
					return 0;
				break;
			case 3:
				if (nY != y - 1)
					return 0;
				break;
		}

		int tempX = x;
		int tempY = y;

		switch (h) {
			case 0:
				tempX--;
				break;
			case 1:
				tempY++;
				break;
			case 2:
				tempX++;
				break;
			case 3:
				tempY--;
				break;
		}

		boolean isFacingWall = isFacingWall(tempX, tempY);

		double walls = 0;

		for (int k = 0; k < 4; k++) {

			tempX = x;
			tempY = y;

			switch (k) {
				case 0:
					tempX--;
					break;
				case 1:
					tempY++;
					break;
				case 2:
					tempX++;
					break;
				case 3:
					tempY--;
					break;
			}

			if (wallForward(tempX, tempY)) {
				walls++;
			}
			if (isInCorner(tempX, tempY)) {
				walls++;
			}

		}

		if (isFacingWall) {
			if (h == nH)
				return 0;
			else
				return 1 / (4 - walls);
		} else {
			if (h == nH)
				return 0.7;
			else
				return 0.3 / (3 - walls);

		}
	}

	public boolean wallForward(int x, int y) {
		return x < 0 || y < 0 || x >= rows || y >= cols;
	}

	public int getDiff(int x1, int x2) {
		return abs(x1-x2);
	}

	public double getOrXY( int rX, int rY, int x, int y, int h) {

		int dX = getDiff(x, rX);
		int dY = getDiff(y, rY);

		if(dX == 0 && dY == 0) {
			return L;
		} else if (dX <= 1 && dY <= 1) {
			return L_s;
		} else if (dX <= 2 && dY <= 2) {
			return L_s2;
		}
		return 0;
	}


	public int[] getCurrentTrueState() {
		
		int[] ret = new int[3];
		ret[1] = currentPosX;
		ret[0] = currentPosY;
		ret[2] = currentHead;

		return ret;
	}


	public int[] getCurrentReading() {
		int[] ret = senseLocation(currentPosX, currentPosY, currentHead);
		return ret;
	}
	// T is static, based on the movement of the robot
	// map index (prob) with position (0,1,LEFT)
	// F = alpha O*T^T*F

	public int[] senseLocation(int x, int y, int h) {
		double rnd = rand.nextDouble();
		Position pos;
		int[] ret = new int[2];
		if(rnd <= L) {
			pos = new Position(x, y, h);
		} else if(rnd <= (L + L_s*5)) {
			pos = getAdjacentPosition(1, currentPosX, currentPosY, currentHead);
		} else if(rnd <= (L + L_s*8 + L_s2*7)) {
			pos = getAdjacentPosition(2, currentPosX, currentPosY, currentHead);
		} else pos = new Position(-1, -1, h);

		if(pos.getX() == -1) {
			ret = null;
		} else {
			ret[0] = pos.getX();
			ret[1] = pos.getY();
		}
		return ret;

	}

	public Position getAdjacentPosition(int layer, int x, int y, int h) {
		Position[] candidates = new Position[8];

		for(int index = 0; index < 8; index++) {
			for (int i = -1; i < 2; i++) {
				for (int j = -1; j < 2; j++) {
					if (validMove(x + i*layer, y + j*layer)) {
						candidates[index] = new Position(x + i*layer, y + j*layer, h);
					} else {
						candidates[index] = new Position(-1, -1, h);
					}
				}
			}
		}
		boolean valid = false;
		Position result = new Position(-1, -1, h);
		int count = 0;

		while(!valid) {
			int rnd = rand.nextInt(8);
			int xPos = candidates[rnd].getX();
			int yPos = candidates[rnd].getY();

			if(validMove(xPos, yPos) && count < 7) {
				valid = true;
				result = candidates[rnd];
			} else {
				return result;
			}
			count ++;
		}
		return result;
	}

	public double getCurrentProb( int x, int y) {
		double sum = 0;

		for(int k = 0; k < head; k++) {
			sum += f[k * cols * rows + x * cols + y][0];
		}
		return sum;
	}

	public boolean validMove(int x, int y) {
		if(x <= this.getNumRows()-1 && y <= this.getNumCols()-1 && x >= 0 && y >= 0) {
			return true;
		}

		return false;
	}

	public boolean isAtWall(int x, int y) {
		if(x == 0 || y == getNumRows()-1 || y == 0 || x == getNumCols()-1) {
			return true;
		}
		return false;
	}

	public boolean isFacingWall(int x, int y) {
		if(isAtWall(x, y)) {
			if(x == 0) {
				if (currentHead == WEST) return true;
			}
			if(x == getNumCols()-1) {
				if (currentHead == EAST) return true;
			}
			if(y == 0) {
				if (currentHead == NORTH) return true;
			}
			if(y == getNumRows()-1) {
				if (currentHead == SOUTH) return true;
			}
		}
		return false;
	}

	public boolean isInCorner(int x, int y) {
		return cornerIndex(x, y) != -1;
	}

	//returns 0 for topleft, 1 for topright, 2 for bottomright, 3 for bottomleft
	//and -1 if not in a corner
	public int cornerIndex(int x, int y) {
		if(x == 0 && y == 0) {
			return 0;
		} else if(x == 0 && y == getNumRows()-1) {
			return 3;
		} else if(x == getNumCols()-1 && y == 0) {
			return 1;
		} else if(x == getNumCols()-1 && y == getNumRows()-1) {
			return 2;
		}

		return -1;
	}

	public int possibleMoves() {
		ArrayList<Integer> moves = new ArrayList<Integer>();
		double rnd = rand.nextDouble();
		int move;
		if (isAtWall(currentPosX, currentPosY) && cornerIndex(currentPosX, currentPosY) == -1) {
			if (currentPosX == 0) {
					moves.add(NORTH);
					moves.add(SOUTH);
					moves.add(EAST);
			}
			if (currentPosX == getNumCols()-1) {
					moves.add(NORTH);
					moves.add(SOUTH);
					moves.add(WEST);
			}
			if (currentPosY == 0) {
					moves.add(EAST);
					moves.add(WEST);
					moves.add(SOUTH);
			}
			if (currentPosY == getNumRows()-1) {
					moves.add(EAST);
					moves.add(WEST);
					moves.add(NORTH);

			}

			int idx = rand.nextInt(moves.size());
			move = moves.get(idx);

		} else if(isAtWall(currentPosX, currentPosY) && cornerIndex(currentPosX, currentPosY) != -1) {
			if(cornerIndex(currentPosX, currentPosY) == 0) {
				moves.add(EAST);
				moves.add(SOUTH);
			} else if(cornerIndex(currentPosX, currentPosY) == 1) {
				moves.add(WEST);
				moves.add(SOUTH);

			} else if(cornerIndex(currentPosX, currentPosY) == 2) {
				moves.add(NORTH);
				moves.add(WEST);

			} else if(cornerIndex(currentPosX, currentPosY) == 3) {
				moves.add(NORTH);
				moves.add(EAST);
			}
			int idx = rand.nextInt(moves.size());
			move = moves.get(idx);

		} else {
			moves.add(SOUTH);
			moves.add(NORTH);
			moves.add(EAST);
			moves.add(WEST);

			if(rnd >= 0.7) {
				int idx = rand.nextInt(moves.size());
				move = moves.get(idx);
			} else {
				move = currentHead;
			}
		}

		return move;
	}

	public boolean move() {
		int temp = currentHead;
		currentHead = possibleMoves();
		switch (currentHead) {
			case 0:
				currentPosY--;
				break;
			case 1:
				currentPosX++;
				break;
			case 2:
				currentPosY++;
				break;
			case 3:
				currentPosX--;
				break;
			default:
		}

		return true;
	}

	public Position moveXY(int x, int y, int h) {
		int tempX = x;
		int tempY = y;
		switch (h) {
			case 0:
				tempY = y-1;
				break;
			case 1:
				tempX = x+1;
				break;
			case 2:
				tempY = y+1;
				break;
			case 3:
				tempX = x-1;
				break;
			default:
		}
		return new Position(tempX, tempY, h);
	}

	public double[][] matrixMultiplication(double[][] A, double[][] B){
		if(A[0].length != B.length) {
			System.out.println("Columns in A did not match rows in B");
			return null;
		}
		double[][] res = new double[A.length][B[0].length];

		for(int i = 0; i < res.length; i++) {
			for(int j = 0; j < res[0].length; j++) {
				for(int k = 0; k < B.length; k++) {
					res[i][j] = res[i][j] + A[i][k] * B[k][j];
				}

			}
		}

		return res;
 	}

 	public double[][] matrixNormalization(double[][] A) {
		double[][] res = new double[A.length][A[0].length];
		double sum = 0;

		for (int i = 0; i < A.length; i++)
		{
			for (int j = 0; j < A[0].length; j++) {
				sum += A[i][j];
			}
		}

		if (sum == 0)
			return A;

		for (int i = 0; i < A.length; i++)
		{
			for (int j = 0; j < A[0].length; j++) {
				res[i][j] = A[i][j] / sum;
			}
		}

		return res;
	}

	public double[][] generateTT() {
		double[][] T = new double[dim][dim];

		for(int hi = 0; hi < head; hi++) {
			for(int ri = 0; ri < rows; ri++) {
				for(int ci = 0; ci < cols; ci++) {
					int i = hi * rows * cols + ci * cols + ri;

					for(int hj = 0; hj < head; hj++) {
						for(int rj = 0; rj < rows; rj++) {
							for(int cj = 0; cj < cols; cj++) {
								int j = hj * rows * cols + cj * cols + rj;

								T[i][j] = getTProb(ci, ri, hi, cj, rj, hj);
							}
						}
					}
				}
			}
		}

		double[][] tTransp = new double[dim][dim];
		for(int r = 0; r < tTransp.length; r++) {
			for(int c = 0; c < tTransp.length; c++) {
				tTransp[r][c] = T[c][r];
			}
		}
		return tTransp;
	}

	public double[][] generateO(int[] state) {
		double[][] o = new double[dim][dim];

		for(int i = 0; i < dim; i++) {
			int col = i / (rows * 4);
			int row = (i / 4) % rows;
			int heading = i % 4;
			o[i][i] = getOrXY(state[0], state[1], row, col, heading);
		}

		return o;
	}

	public void update() {
		clicks++;
		int[] est = getCurrentReading();
		move();


		if(est != null) {
			double[][] O = generateO(est);
			double[][] OTT = matrixMultiplication(O, TT);
			double[][] OTTf = matrixMultiplication(OTT, f);
			f = matrixNormalization(OTTf);

			int dX = getDiff(currentPosX, est[0]);
			int dY = getDiff(currentPosY, est[1]);

			manhattan += dX+dY;

		} else {
			manhattan += 0;
			double[][] TTf = matrixMultiplication(TT, f);
			f = matrixNormalization(TTf);
		}
		System.out.println("mean distance = " + manhattan/clicks);





	}
	
	
}

class Position {
	private int x;
	private int y;
	private int h;

	public Position(int x, int y, int h) {
		this.x = x;
		this.y = y;
		this.h = h;
	}

	public int getX() { return x; }

	public int getY() { return y; }

	public int getH() { return h; }
}