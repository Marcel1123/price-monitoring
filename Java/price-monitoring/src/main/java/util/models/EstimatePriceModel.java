package util.models;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import util.enums.FurnishType;
import util.enums.ProductType;

import java.io.Serializable;
import java.util.UUID;

@Getter
@Setter
@Builder
public class EstimatePriceModel implements Serializable {
    private ProductType product_type;
    private FurnishType furnish_type;
    private double size;
    private int number_of_rooms;
    private int floor_number;
    private int number_of_floors;
    private int year_of_construction;
    private UUID location_id;
}
