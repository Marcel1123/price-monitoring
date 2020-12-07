package page.classes;

import entities.LocationEntity;
import lombok.Getter;
import lombok.Setter;
import util.enums.ProductType;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import java.io.Serializable;

@ManagedBean
@RequestScoped
@Getter
@Setter
public class Product implements Serializable {
    private LocationEntity location;
    private int numberOfRooms;
    private ProductType type;
    private double size;
    private int floorNumber;
    private int numberOfFloors;
    private int yearOfConstruction;

    public void estimation(){

    }
}
