package page.classes;

import entities.ProductEntity;
import lombok.Getter;
import lombok.Setter;
import page.classes.selectors.SelectedFields;

import java.io.Serializable;

@Getter
@Setter
public class Information implements Serializable {
    private SelectedFields selectedFields;
    private ProductEntity productEntity;
    private String location;

    public Information(){
        selectedFields = new SelectedFields();
        productEntity = new ProductEntity();
    }
}
