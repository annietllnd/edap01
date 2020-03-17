package model;

public enum Direction {
    NORTH, EAST, SOUTH, WEST;

    public int dx() {
        if(this == EAST) {
            return 1;
        }
        if(this == WEST) {
            return -1;
        }
        return 0;
    }

    public int dy() {
        if(this == SOUTH) {
            return 1;
        }
        if(this == NORTH) {
            return -1;
        }
        return 0;
    }
}
